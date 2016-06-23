'use strict';
if (Meteor.isClient) {
	Meteor.subscribe('nextPlayingPoolsByUserId');
	//init
	//events
	//helpers
	Template.nextPools.helpers({
		pools: function() {
			return Pools.find({
				matchDate: {
					$gte : new Date()
				}
			});
		}
	});
}
