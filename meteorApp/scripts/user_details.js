'use strict';
Router.route('/user/:id', function () {
	this.render('userDetails', {
		data: function () {
			return Meteor.users.findOne({_id : this.params.id});
		}
	});
},{ 
	name: 'userDetails',
	waitOn: function() {
		return [
			Meteor.subscribe('userById', this.params.id)
		];
	},
	onBeforeAction: function() {
		if (!Meteor.user()) {
			this.render('landing');
		}
		else {
			this.next();
		}
	}
});

if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.userDetails.helpers({
		email: function() {
			return this.emails[0].address
		}
	});
}
