Router.route('/user', { 
		name: 'user',
		template: 'user',
	});

if (Meteor.isClient) {

	//init
	//events
	//helpers

	Template.user.helpers({
		log: function(){
			console.log(this);
			return this;
		}
	});
}
