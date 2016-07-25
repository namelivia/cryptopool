from scrapper_la_liga_oficial.matchUpdater import MatchUpdater
from scrapper_la_liga_oficial.usersCollectionManager import UsersCollectionManager
from scrapper_la_liga_oficial.poolsCollectionManager import PoolsCollectionManager
from scrapper_la_liga_oficial.teamsCollectionManager import TeamsCollectionManager
from scrapper_la_liga_oficial.matchesCollectionManager import MatchesCollectionManager
from random import randint
from faker import Faker
from random import randint
import datetime

fake = Faker()
usersCollectionManager = UsersCollectionManager()
poolsCollectionManager = PoolsCollectionManager()
poolsCollectionManager = PoolsCollectionManager()
matchesCollectionManager = MatchesCollectionManager()
teamsCollectionManager = TeamsCollectionManager()
matchUpdater = MatchUpdater()

def main():
	create_a_random_match()
	make_a_random_user()
	make_a_random_pool()
	make_a_random_bet()

def make_a_random_user():
	print("Creating a random user")
	email = fake.email()
	newUser = {
			"services" : { 
				"password" : { "bcrypt" : "$2a$10$VxfCnQmcDKYcIGy0C3eecOehWuvQ3lWLWPga7peJKJY1hXf1qqhzu" },
				"email" : { 
					"verificationTokens" : []
				},
				"resume" : { 
					"loginTokens" : [ ] 
				} 
			},
			"username" : fake.word(),
			"emails" : [ { "verified" : True, "address" : email} ],
			"tokens" : 10, "poolHistory" : [] }
	usersCollectionManager.insert_a_new_user(newUser)

def make_a_random_pool():
	print("Creating a random pool")
	#pick a random user
	user = usersCollectionManager.get_a_random_user()
	if user is not None :
		match = matchesCollectionManager.get_a_random_unplayed_match()
		if match is not None :
			newPool = {
				"amount" :randint(1, 9),
				"match_id" : match['_id'],
				"status_id" : 0,
				"user_id" : user['_id'],
				"users" : [],
				"matchDate" : match['date']
			}
			poolsCollectionManager.insert_a_new_pool(newPool)
		else:
			print("There are no matches")
	else:
		print("There are no users")


def create_a_random_match():
	print("Creating a random match")
	player1Id = teamsCollectionManager.get_a_random_team()['_id'];
	player2Id = teamsCollectionManager.get_a_random_team()['_id'];
	if player1Id is not None and player2Id is not None :
		match = {
			'player1' : player1Id,
			'player2' : player2Id,
			'date' : datetime.datetime.now(),
			'score1' : '',
			'score2' : '',
			'status' : 0,
			'referee' : fake.name(),
			'hashtag' : '#Madrid'
		}
		matchUpdater.create_or_update_the_match(match)
	else:
		print("There are no teams")

def make_a_random_bet():
	print("Making a random bet")
	#pick a random user
	user = usersCollectionManager.get_a_random_user()
	if user is not None :
	#pick a random bet for less than the user tokens
		pool = poolsCollectionManager.get_a_random_open_pool_for_tokens(user['tokens'])
		if pool is not None :
			user['tokens'] -= pool['amount']
			user['poolHistory'].append(pool['_id'])
			newEntry = {
					'_id' : user['_id'],
					'localScore' : randint(0,3),
					'visitantScore' : randint(0,3)
			}
			pool['users'].append(newEntry)
			usersCollectionManager.update_an_existing_user(user)
			poolsCollectionManager.update_an_existing_pool(pool)
		else:
			print("There are no pools")
	else:
		print("There are no users")

if __name__ == "__main__":
	main()
