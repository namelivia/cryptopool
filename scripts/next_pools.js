'use strict';
if (Meteor.isClient) {
	Meteor.subscribe('nextPools');
	//init
	//events
	//helpers
	Template.nextPools.helpers({
		matches: function() {
			return Pools.find(
				{ date : { 
					$gte : new Date()
						}
				},{
					limit : 5
				}
			);
		}
	});
}
