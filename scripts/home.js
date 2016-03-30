'use strict';
Router.route('/', {
	name: 'home',
	template: 'home',
	waitOn: function() {
		return [
			Meteor.subscribe('teams')/*,
			Meteor.subscribe('poolsByUserId')*/
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

	Template.home.helpers({
		/*poolHistory: function(){
			return Pools.find();
		}*/
	});
}
