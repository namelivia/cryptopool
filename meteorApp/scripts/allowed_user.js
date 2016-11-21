'use strict';
if (Meteor.isClient) {
	//init
	//events
	Template.allowed_user.events({
		"click .allow": function (event) {
			event.preventDefault();
			var userId = event.target.attributes.getNamedItem('data-userid').value;
			var poolId = event.target.attributes.getNamedItem('data-poolid').value;
			Meteor.call('allowUserToPool',userId,poolId,function(error){
				if (error) {
					toastr.error(error.details, error.reason);
				} else {
					toastr.success(
							'You have allowed the user to the pool',
							'Access allowed'
					);
				}
			});
		},
		"click .deny": function (event) {
			event.preventDefault();
			var userId = event.target.attributes.getNamedItem('data-userid').value;
			var poolId = event.target.attributes.getNamedItem('data-poolid').value;
			Meteor.call('denyUserToPool',userId,poolId,function(error){
				if (error) {
					toastr.error(error.details, error.reason);
				} else {
					toastr.success(
							'You have denied the user to the pool',
							'Access denied'
					);
				}
			});
		}
	});
	//helpers
	Template.allowed_user.helpers({
		isPending: function() {
			return this.confirmed === null;
		},
		isApproved: function() {
			return this.confirmed === true;
		},
		isDenied: function() {
			return this.confirmed === false;
		}
	});
}
