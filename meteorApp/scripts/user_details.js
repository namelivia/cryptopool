'use strict';
Router.route('/user/:id', function () {
	this.render('userDetails', {
		data: function () {
			var oid = new Meteor.Collection.ObjectID(this.params.id);
			return Meteor.users.findOne({_id : oid});
		}
	});
},{ 
	name: 'userDetails',
	waitOn: function() {
		var oid = new Meteor.Collection.ObjectID(this.params.id);
		return [
			Meteor.subscribe('userById',oid)
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
