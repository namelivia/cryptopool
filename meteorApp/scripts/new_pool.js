'use strict';
if (Meteor.isClient) {
	//init
	//events
	Template.newPool.events({
		'submit .new-pool': function (event) {
			event.preventDefault();
			var amount = parseInt(event.target.amount.value);
			var isPrivate = event.target.private.checked === true;
			var isMultiuser = event.target.multiuser.checked === true;
			var isMultiscore = event.target.multiscore.checked === true;
			var isClosest = event.target.closest.checked === true;
			Meteor.call('createPool',amount,isPrivate,isMultiuser,isMultiscore,isClosest,this.matchId,function(error,response){
				if (error){
					toastr.error(error.details, error.reason);
				} else {
					var successMsg = 'You have successfully created a';
				  	successMsg += isPrivate ? ' private ' : ' public ';	
					successMsg += amount;
					successMsg += ' token pool';
					toastr.success(successMsg, 'Pool created');
				}
			});
			Modal.hide();
		}
	});
	//helpers
}
