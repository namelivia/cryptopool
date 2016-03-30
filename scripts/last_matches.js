'use strict';
if (Meteor.isClient) {
	Meteor.subscribe('lastMatches');
	//init
	//events
	//helpers
	Template.lastMatches.helpers({
		matches: function() {
			return Matches.find(
				{date : { 
					$lte : new Date()
						}
				},{ 
					limit : 5, sort : { date: -1 }
				}
			);
		}
	});
}
