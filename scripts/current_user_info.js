if (Meteor.isClient) {

	//init
	Template.currentUserInfo.onCreated(function() {
		var self = this;
		this.autorun(function() {
			self.subscribe('userData');  
		});
	});
	//events
	//helpers

	Template.currentUserInfo.helpers({
		userTokens: function(){
			return Meteor.user().tokens;
		},
		userUsername: function(){
			return Meteor.user().username;
		},
	});
}
