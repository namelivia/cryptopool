from scrapper_la_liga_oficial.usersCollectionManager import UsersCollectionManager
from scrapper_la_liga_oficial.poolsCollectionManager import PoolsCollectionManager
from random import randint
from faker import Faker

fake = Faker()
usersCollectionManager = UsersCollectionManager()
poolsCollectionManager = PoolsCollectionManager()

def main():
	make_a_random_user()
	make_a_random_bet()

def make_a_random_user():
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

def make_a_random_bet():
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

if __name__ == "__main__":
	main()
