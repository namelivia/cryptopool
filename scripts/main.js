Matches = new Mongo.Collection("matches");
Teams = new Mongo.Collection("teams");
Pools = new Mongo.Collection("pools");

Router.configure({
	    layoutTemplate: 'main'
});

if (Meteor.isClient) {
	Session.set("searchDate", new Date());

	//Suscribe to the collections
	Meteor.subscribe("userData");
	Meteor.subscribe("matches");
	Meteor.subscribe("teams");
	Meteor.subscribe("pools");
	Meteor.subscribe("findOneMatch");
}

if (Meteor.isServer) {
	Meteor.startup(function () {
		// code to run on server at startup
	});

	//Publish the public collections
	Meteor.publish("matches", function () {
		return Matches.find();
	});

	Meteor.publish("teams", function () {
		return Teams.find();
	});

	Meteor.publish("pools", function () {
		return Pools.find();
	});

	Meteor.publish("findOneMatch", function (matchId) {
		return Matches.find({_id : matchId});
	});

	// Extending the user model
	Accounts.onCreateUser(function(options, user) {
		user.tokens = 10;
		// We still want the default hook's 'profile' behavior.
		if (options.profile)
			user.profile = options.profile;
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
