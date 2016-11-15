'use strict';
if (Meteor.isClient) {

	//init
	Template.currentUserInfo.onCreated(function() {
		var self = this;
		this.autorun(function() {
			self.subscribe('userById'),
			self.subscribe('myNotifications')
		});
	});
	//events
	//helpers

	Template.currentUserInfo.helpers({
		userTokens: function(){
			return Meteor.user().tokens;
		},
		userUsername: function(){
			return Meteor.user().username;
		},
		userId: function(){
			return Meteor.user()._id;
		},
		notificationCount: function(){
			return Notifications.find({seen : false}).count();
		}
	});
}
