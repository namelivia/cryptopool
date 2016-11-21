'use strict';
Router.route('/match/:matchId/pool/:id/admin', function () {
	this.render('poolAdmin', {
		data: function () {
			var oid = new Meteor.Collection.ObjectID(this.params.id);
			var pool = Pools.findOne({_id : oid});
			var users = Meteor.users.find();
			return {
				pool : pool,
				users : users
			};
		}
	});
},{ 
	name: 'poolAdmin',
	waitOn: function() {
		var oid = new Meteor.Collection.ObjectID(this.params.id);
		return [
			Meteor.subscribe('poolById',oid),
			Meteor.subscribe('usersByPoolId',oid)
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
	Template.poolAdmin.events({
	});
	//helpers
	Template.poolAdmin.helpers({
		allowed_users: function() {
			var poolId = this.pool._id._str;
			return _.map(this.pool.allowed_users, function (user) {
				user.poolId = poolId;
				return user;
			})
		}
	});
}
