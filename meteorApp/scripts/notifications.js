'use strict';
Router.route('/notifications', function () {
	this.render('notifications', {
		data: function () {
			return Notifications.find({user_id : Meteor.user()._id});
		}
	});
},{ 
	name: 'notifications',
	waitOn: function() {
		return [
			Meteor.subscribe('myNotifications')
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
	Template.notifications.helpers({
		notifications: function() {
			return this;
		}
	});
}
