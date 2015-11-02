Teams = new Mongo.Collection("teams");
Pools = new Mongo.Collection("pools");
Matches = new Mongo.Collection("matches");

Router.configure({
	    layoutTemplate: 'main'
});

if (Meteor.isClient) {
	Session.set("searchDate", new Date());
}

if (Meteor.isServer) {
	Meteor.startup(function () {
		// code to run on server at startup
	});

	Meteor.methods({
		makeBitcoinAddress: function () {
			try {
				var privKey = bitcoinjs.ECKey.makeRandom();
				return {privKey: privKey.toWIF()};
			} catch (e) {
				throw Meteor.Error('some-error', 'Bad things happened.');
			}
		}
	});

	//Publish the public collections
	Meteor.publish("nextMatches", function () {
		var nextMatches = Matches.find(
			{date : { 
				$gt : new Date()
					}
			},{limit : 5});
		return nextMatches
	});

	Meteor.publish("matchesByDateRange", function (startDate,endDate) {
		return Matches.find(
				{date : { 
							$gte : new Date(startDate),
							$lte : new Date(endDate)
						}
				});
	});

	Meteor.publish("poolsByMatchId", function (matchId) {
		return Pools.find({match_id : matchId});
	});

	Meteor.publish("matchById", function (matchId) {
		return Matches.find({_id : matchId});
	});

	Meteor.publish("poolById", function (poolId) {
		return Pools.find({_id : poolId});
	});

	Meteor.publish("lastMatches", function () {
		return Matches.find(
			{date : { 
				$lt : new Date()
					}
			},{ limit : 5, sort : { date: -1 }}
		);
	});

	Meteor.publish("teams", function () {
		return Teams.find();
	});

	// Extending the user model
	Accounts.onCreateUser(function(options, user) {
		user.tokens = 10;
		// We still want the default hook's 'profile' behavior.
		if (options.profile) {
			user.profile = options.profile;
		}
		return user;
	});

	Meteor.publish("userData", function () {
		if (this.userId) {
			return Meteor.users.find({_id: this.userId},
					{fields: {'tokens': 1}});
		} else {
			this.ready();
		}
	});
}
