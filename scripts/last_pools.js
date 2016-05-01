'use strict';
if (Meteor.isClient) {
	Meteor.subscribe('lastPlayedPoolsByUserId');
	//init
	//events
	//helpers
	Template.lastPools.helpers({
		pools: function() {
			return Pools.find();
		}
	});
}
