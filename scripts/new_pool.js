if (Meteor.isClient) {
	//init
	//events
	Template.newPool.events({
		"submit .new-pool": function (event) {
			event.preventDefault();
			var amount = parseInt(event.target.amount.value);
			Meteor.call('createPool',amount,this.matchId,function(error,response){
				if (error){
					toastr.error(error.details, error.reason);
				} else {
					toastr.success('You have successfully created a '+amount+' token pool', 'Pool created');
				}
			});
			Modal.hide();
		}
	});
	//helpers
}
