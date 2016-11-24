'use strict';
Router.route('/match/:matchId/pool/:id/admin', function () {
	this.render('poolAdmin', {
		data: function () {
			var oid = new Meteor.Collection.ObjectID(this.params.id);
			var pool = Pools.findOne({_id : oid});
			var matchId = this.params.matchId;
			return {
				pool : pool,
				matchId : matchId
			};
		}
	});
},{ 
	name: 'poolAdmin',
	waitOn: function() {
		var oid = new Meteor.Collection.ObjectID(this.params.id);
		return [
			Meteor.subscribe('poolById',oid),
			Meteor.subscribe('allowedUsersByPoolId',oid)
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
			var matchId = this.matchId;
			return _.map(this.pool.allowed_users, function (user) {
				user.poolId = poolId;
				user.matchId = matchId;
				user.user = Meteor.users.findOne({_id : user.id});
				return user;
			});
		}
	});

}
