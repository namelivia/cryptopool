'use strict';
Router.route('/my_profile', function () {
	this.render('myProfile', {
		data: function () {
			return Meteor.users.findOne({});
		}
	});
},{ 
	name: 'myProfile',
	waitOn: function() {
		return [
			Meteor.subscribe('userById')
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

	Template.myProfile.helpers({
		email: function() {
			return this.emails[0].address
		},
		poolHistory: function(){
			return Pools.find();
		}
	});
}
