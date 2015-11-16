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
				console.log(error);
				if (error){
					Flash.error("__default__",error.reason,3000,true);
				} else {
					Flash.success("__default__",'You have joined the pool',3000,true);
				}
			});
			Modal.hide();
		}
	});
}
