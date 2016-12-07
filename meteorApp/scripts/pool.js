'use strict';
if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.user.helpers({
		isWinner : function() {
			return this.winner ? 'Yes' : 'No';
		}
	});
}
