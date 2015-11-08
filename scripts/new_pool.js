if (Meteor.isClient) {
	//init
	//events
	Template.newPool.events({
		"submit .new-pool": function (event) {
			event.preventDefault();
			var amount = parseInt(event.target.amount.value);
			Meteor.call('createPool',amount,this.matchId);
			Modal.hide();
			Flash.success("__default__",'Pool successfully created',3000,true);
		}
	});
	//helpers
}
