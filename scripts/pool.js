if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.pool.helpers({
		userCount : function() {
			return this.users.length;
		}
	});
}
