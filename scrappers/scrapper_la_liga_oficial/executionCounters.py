class ExecutionCounters:
	counters = {
		'newMatchesCounter' : 0,
		'newTeamsCounter' : 0,
		'updatedMatchesCounter' : 0,
		'matchesWithoutHashtag' : 0,
		'matchesWithoutLink' : 0,
		'newCompetitionsCounter' : 0,
	}

	def increase_matches_without_hashtag_counter(self):
		self.counters['matchesWithoutHashtag'] += 1

	def increase_new_teams_counter(self):
		self.counters['newTeamsCounter'] += 1

	def increase_new_matches_counter(self):
		self.counters['newMatchesCounter'] += 1

	def increase_new_competitions_counter(self):
		self.counters['newCompetitionsCounter'] += 1

	def increase_updated_matches_counter(self):
		self.counters['updatedMatchesCounter'] += 1

	def increase_matches_without_link_counter(self):
		self.counters['matchesWithoutLink'] += 1

	def get_counters(self):
		return self.counters
