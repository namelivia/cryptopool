'use strict';
Router.route('/teams', { 
	name: 'teams',
	template: 'teams',
	waitOn: function() {
		return [
			Meteor.subscribe('teams')
		];
	},
	onBeforeAction: function() {
		if (!Meteor.user()) {
			this.render('landing');
		}
		else {
			this.next();
		}
	}
});

if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.teams.helpers({
		teams: function() {
			return Teams.find();
		}
	});
}
