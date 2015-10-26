if (Meteor.isClient) {
	Meteor.subscribe("nextMatches");
	//init
	//events
	//helpers
	Template.nextMatches.helpers({
		matches: function() {
			var test = Matches.find(
				{date : { 
					$gte : new Date()
						}
				},{limit : 5}
			);
			return test;
		}
	});
}
