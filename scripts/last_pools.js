'use strict';
if (Meteor.isClient) {
	Meteor.subscribe('lastPools');
	//init
	//events
	//helpers
	Template.lastPools.helpers({
		pools: function() {
			return Pools.find(
				{ date : {
					$lte:new Date()
						 }
				},{
					limit:5, sort: {
						date:-1
					}
				}
			);
		}
	});
}
