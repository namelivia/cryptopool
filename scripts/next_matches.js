if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.nextMatches.helpers({
		matches: function() {
			return Matches.find(
				{date : { 
					$gte : new Date()
						}
				},{limit : 5});
		},
		upcomingMatches: function() {
			//http://stackoverflow.com/questions/18413457/meteor-template-pass-a-parameter-into-each-sub-template-and-retrieve-it-in-the
			return _.extend({context:"upcomingMatches"},this);
		}
	});
}
