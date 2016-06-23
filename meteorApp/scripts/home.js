'use strict';
Router.route('/', {
	name: 'home',
	template: 'home',
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
}
