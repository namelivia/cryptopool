if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.confirmJoin.events({
		"submit .join-pool": function (event) {
			event.preventDefault();
			var localScore = parseInt(event.target.localScore.value);
			var visitantScore = parseInt(event.target.visitantScore.value);
			Meteor.call('joinPool',this._id,localScore,visitantScore);
			Modal.hide();
			Flash.success("__default__",'You have joined the pool',3000,true);
		}
	});
}
