if (Meteor.isClient) {
	//init
	//events
	Template.poolList.events({
		"click .new_pool": function (event) {
			event.preventDefault();
			Modal.show('newPool',{ matchId : this.matchId })
		}
	});
	//helpers
}
