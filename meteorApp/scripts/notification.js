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
			switch (this.key) {
				case 'newMessage':
					return 'You have a new private message from '+this.data.username
				case 'newAccessRequest':
					return this.data.username+' is waiting to be approved on one of your pools'
				default:
					return 'Unknown notification';
			}
		},
		notificationId : function() {
			return this._id._str;
		},
		alreadySeen: function() {
			return this.seen;
		}
	});
}
