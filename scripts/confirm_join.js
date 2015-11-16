if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.confirmJoin.events({
		"submit .join-pool": function (event) {
			event.preventDefault();
			var localScore = parseInt(event.target.localScore.value);
			var visitantScore = parseInt(event.target.visitantScore.value);
			Meteor.call('joinPool',this._id,localScore,visitantScore,function(error,response){
				if (error) {
					toastr.error(error.details, error.reason);
				} else {
					toastr.success('You have successfully joined to the pool', 'You have joined to the pool');
				}
			});
			Modal.hide();
		}
	});
}
