import unittest2 as unittest
import mock
import mongomock
from scrapperLaLigaOficial import ScrapperLaLigaOficial
from lxml import html
from datetime import datetime 
import time
import io

class scrapperLaLigaOficialTest(unittest.TestCase):

	def setUp(self):
		self.scrapper = ScrapperLaLigaOficial()

	def test_extracting_the_referee_from_a_match(self):
		htmlString = """
		fooBarfooBar
			<span class="arbitro last">Referee1</span>
		fooBarfooBar
		""";
		tree = html.fromstring(htmlString)
		self.assertEqual('Referee1',self.scrapper.extract_referee(tree))

	def test_extracting_the_match_date_and_hour(self):
		htmlString = """
		fooBarfooBar
			<span class="fecha left">
				<span class="dia">15-12-2016</span>
				<span class="hora">aa12:00 </span>
			</span>
		fooBarfooBar
		""";
		tree = html.fromstring(htmlString)
		matchDate = self.scrapper.extract_match_date(tree)
		expectedDate = datetime(2016, 12, 15, 12, 00, 00)
		self.assertEqual(expectedDate,matchDate)

	def test_extracting_the_match_date_without_hour(self):
		htmlString = """
		fooBarfooBar
			<span class="fecha left">
				<span class="dia">15-12-2016</span>
				<span class="hora"></span>
			</span>
		fooBarfooBar
		""";
		tree = html.fromstring(htmlString)
		matchDate = self.scrapper.extract_match_date(tree)
		expectedDate = datetime(2016, 12, 15, 00, 00, 00)
		self.assertEqual(expectedDate,matchDate)

	def test_extracting_the_local_team_from_a_match_when_the_team_is_present(self):
		teams = [dict(name="FooTeam")];
		teamsCollection = mongomock.MongoClient().db.collection
		for team in teams:
			team['_id'] = teamsCollection.insert(team)
		htmlString = """
		fooBarfooBar
			<span class="equipo left local">
				<span class="team">FooTeam</span>
			</span>
		fooBarfooBar
		""";
		tree = html.fromstring(htmlString)
		newTeam = self.scrapper.extract_team(tree,True,teamsCollection,5)
		self.assertEqual(5,newTeam[0])
		self.assertEqual(teams[0]['_id'],newTeam[1])

	def test_extracting_the_local_team_from_a_match_when_the_team_is_not_present(self):
		teamsCollection = mongomock.MongoClient().db.collection
		htmlString = """
		fooBarfooBar
			<span class="equipo left local">
				<span class="team">FooTeam</span>
			</span>
		fooBarfooBar
		""";
		tree = html.fromstring(htmlString)
		newTeam = self.scrapper.extract_team(tree,True,teamsCollection,5)
		self.assertEqual(6,newTeam[0])
		insertedTeam = teamsCollection.find_one({'_id' : newTeam[1]}) 
		self.assertEqual('FooTeam',insertedTeam['name'])
		self.assertEqual('footeam',insertedTeam['tag'])

	def test_tag_formation_for_spaces(self):
		teamsCollection = mongomock.MongoClient().db.collection
		htmlString = """
		fooBarfooBar
			<span class="equipo left local">
				<span class="team">Foo Team</span>
			</span>
		fooBarfooBar
		""";
		tree = html.fromstring(htmlString)
		newTeam = self.scrapper.extract_team(tree,True,teamsCollection,5)
		self.assertEqual(6,newTeam[0])
		insertedTeam = teamsCollection.find_one({'_id' : newTeam[1]}) 
		self.assertEqual('Foo Team',insertedTeam['name'])
		self.assertEqual('foo_team',insertedTeam['tag'])

	def test_tag_formation_for_points(self):
		teamsCollection = mongomock.MongoClient().db.collection
		htmlString = """
		fooBarfooBar
			<span class="equipo left local">
				<span class="team">Fc. Foo Team</span>
			</span>
		fooBarfooBar
		""";
		tree = html.fromstring(htmlString)
		newTeam = self.scrapper.extract_team(tree,True,teamsCollection,5)
		self.assertEqual(6,newTeam[0])
		insertedTeam = teamsCollection.find_one({'_id' : newTeam[1]}) 
		self.assertEqual('Fc. Foo Team',insertedTeam['name'])
		self.assertEqual('fc_foo_team',insertedTeam['tag'])

	def test_tag_formation_for_the_real_keyword(self):
		teamsCollection = mongomock.MongoClient().db.collection
		htmlString = """
		fooBarfooBar
			<span class="equipo left local">
				<span class="team">R. Foo Team</span>
			</span>
		fooBarfooBar
		""";
		tree = html.fromstring(htmlString)
		newTeam = self.scrapper.extract_team(tree,True,teamsCollection,5)
		self.assertEqual(6,newTeam[0])
		insertedTeam = teamsCollection.find_one({'_id' : newTeam[1]}) 
		self.assertEqual('R. Foo Team',insertedTeam['name'])
		self.assertEqual('real_foo_team',insertedTeam['tag'])

	def test_finding_the_data_on_the_page(self):
		page = """
		<html>
			<script>script1</script>
			<script>script2script2script2</script>
			<script>
				script3
				script3
				script3
				0123456789012345script3longestline78
			</script>
			<script>script4</script>
			<script>script5</script>
			<script>script6</script>
			<script>script7</script>
			<script>script8</script>
		</html>
		"""
		data = self.scrapper.data_find(page)
		self.assertEqual('script3longestline',data)

	@mock.patch('scrapper_la_liga_oficial.scrapperLaLigaOficial.time.time')
	@mock.patch('scrapper_la_liga_oficial.scrapperLaLigaOficial.requests.get')
	@mock.patch('scrapper_la_liga_oficial.scrapperLaLigaOficial.requests.post')
	@mock.patch('scrapper_la_liga_oficial.scrapperLaLigaOficial.ScrapperLaLigaOficial.data_find')
	def test_scrapping(self, mock_data_find, mock_requests_post, mock_requests_get, mock_time):
		calendarUrl = 'http://www.laliga.es/calendario-horario/';
		eventId = u'#1_1_1_10_8_2016';
		eventUrl = 'http://www.laliga.es/includes/ajax.php?action=ver_evento_calendario';
		mock_data_find.return_value = '[{"url" : "'+eventId+'"}]'
		mock_requests_get.return_value.text = self.get_html_example(calendarUrl)
		mock_requests_post.return_value.text = self.get_html_example(eventUrl)
		mock_time.return_value = time.mktime(datetime(2016, 8, 15, 12, 00, 00).timetuple())
		self.scrapper = ScrapperLaLigaOficial()
		test = self.scrapper.start_scrapping(5)
		mock_time.assert_called_with()
		mock_requests_get.assert_called_with(calendarUrl)
		mock_requests_post.assert_called_with(eventUrl, data={'filtro': eventId})

	#Aux functions
	def get_html_example(self, url):
		examples = {
			'http://www.laliga.es/calendario-horario/' : 'calendario-horario.html',
			'http://www.laliga.es/includes/ajax.php?action=ver_evento_calendario' : 'ver-evento-calendario.html',
		}
		with io.open('request_examples/'+examples[url], 'r', encoding='utf-8') as myfile:
			data = myfile.read().replace('\n', '')
		return data

if __name__ == '__main__':
	unittest.main()
