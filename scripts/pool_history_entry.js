'use strict';
if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.poolHistoryEntry.helpers({
		poolId: function() {
			return this.pool._id._str;
		},
		matchId: function() {
			return this.pool.match_id._str;
		}
	});
}
