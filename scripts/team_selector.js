if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.teamSelector.helpers({
		teams : function () {
			return Teams.find({});
		},
	});
}
