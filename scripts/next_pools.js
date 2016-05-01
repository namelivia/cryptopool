'use strict';
if (Meteor.isClient) {
	Meteor.subscribe('nextPlayingPoolsByUserId');
	//init
	//events
	//helpers
	Template.nextPools.helpers({
		pools : function() {
			var pools = Pools.find();
			console.log(pools);
			return pools;
		}
	});
}
