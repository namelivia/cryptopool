'use strict';
if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.message.helpers({
		from : function() {
			return this.fromUser().username;
		}
	});
}
