Router.route('/user', { 
		name: 'user',
		template: 'user',
	});

if (Meteor.isClient) {

	//init
	//events
	//helpers

	Template.user.helpers({
		tokens: function(){
			return Meteor.user().tokens;
		}
	});
}
