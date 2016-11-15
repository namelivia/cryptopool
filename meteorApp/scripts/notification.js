'use strict';
if (Meteor.isClient) {
	//init
	//events
	Template.notification.events({
		"click .toggleSeen": function (event) {
			event.preventDefault();
			var notificationId = event.target.attributes.getNamedItem('data-notificationid').value;
			Meteor.call('toggleNotificationAsSeen',notificationId,function(error){
				if (error) {
					toastr.error(error.details, error.reason);
				} else {
					toastr.success(
							'You have marked the notification as seen',
							'Notification marked as seen'
					);
				}
			});
		}
	});
	//helpers
	Template.notification.helpers({
		content: function() {
			if (this.key === 'newMessage') {
				return 'You have a new private message from '+this.data.username
			}
			return 'Unknown notification';
		},
		notificationId : function() {
			return this._id._str;
		},
		alreadySeen: function() {
			return this.seen;
		}
	});
}
