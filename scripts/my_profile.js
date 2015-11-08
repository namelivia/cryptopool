Router.route('/my_profile', { 
	name: 'myProfile',
	waitOn: function() {
		return [
			Meteor.subscribe('userData')
		]
	}
});

if (Meteor.isClient) {

	//init
	//events
	//helpers

	Template.myProfile.helpers({
		userEmail: function(){
			return Meteor.user().emails[0].address;
		},
		userTokens: function(){
			return Meteor.user().tokens;
		},
		userUsername: function(){
			return Meteor.user().username;
		},
		poolHistory: function(){
			return Meteor.user().poolHistory;
		},
	});
}
