if (Meteor.isClient) {
	Meteor.subscribe("nextMatches");
	//init
	//events
	//helpers
	Template.nextMatches.helpers({
		matches: function() {
			return Matches.find(
				{date : { 
					$gte : new Date()
						}
				},{limit : 5}
			)
		}
	});
}
