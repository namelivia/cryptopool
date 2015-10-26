Router.route('/', {
	name: 'home',
	template: 'home',
	waitOn: function() {
		return [
			Meteor.subscribe('teams')
		]
	},
	onBeforeAction: function() {
		this.next();
	}
});

if (Meteor.isClient) {
	
	//init

	//events

	//helpers

	Template.home.helpers({
	});
}
