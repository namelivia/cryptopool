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

	/*Meteor.publish("pools", function () {
		return Pools.find();
	});*/

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
