Matches = new Mongo.Collection("matches");
Teams = new Mongo.Collection("teams");

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
}
