'use strict';
if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.pool.helpers({
		betCount : function() {
			return this.users.length;
		},
		isPrivate : function() {
			return this.options.is_private ? 'Yes' : 'No';
		},
		isMultiscore: function() {
			return this.options.multiscore ? 'Yes' : 'No';
		},
		isMultibet: function() {
			return this.options.multiuser ? 'Yes' : 'No';
		},
		isClosest: function() {
			return this.options.closest ? 'Yes' : 'No';
		}
	});
}
