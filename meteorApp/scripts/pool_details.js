'use strict';
Router.route('/match/:matchId/pool/:id', function () {
	this.render('poolDetails', {
		data: function () {
			var oid = new Meteor.Collection.ObjectID(this.params.id);
			var pool = Pools.findOne({_id : oid});
			var users = Meteor.users.find();
			var matchId = this.params.matchId;
			return {
				pool : pool,
				users : users,
				matchId : matchId
			};
		}
	});
},{ 
	name: 'poolDetails',
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
	Template.poolDetails.events({
		"click .join": function (event) {
			event.preventDefault();
			Modal.show('confirmJoin',{ _id : this.pool._id });
		},
		"click .request-access": function (event) {
			event.preventDefault();
			Meteor.call('requestPoolAccess',this.matchId,this.pool._id,function(error,response){
				if (error){
					toastr.error(error.details, error.reason);
				} else {
					toastr.success('You have requested access to the pool', 'Access requested');
				}
			});
		},
	});
	//helpers
	Template.poolDetails.helpers({
		betCount : function() {
			return this.pool.users.length;
		},
		amIAllowed : function() {
			if (this.pool.options.is_private) {
				var foundUser = _.find(this.pool.allowed_users, function(user){
					return user.id === Meteor.user()._id;
				});
				if (foundUser === undefined || foundUser.confirmed !== true) { 
					return false;
				}
			}
			return true;
		},
		amIRejected: function() {
			if (this.pool.options.is_private) {
				var foundUser = _.find(this.pool.allowed_users, function(user){
					return user.id === Meteor.user()._id;
				});
				if (foundUser !== undefined && foundUser.confirmed === false) { 
					return true;
				}
			}
			return false;
		},
		amIAdmin: function() {
			return this.pool.user_id === Meteor.user()._id;
		},
		amIWaiting : function() {
			if (this.pool.options.is_private) {
				var foundUser = _.find(this.pool.allowed_users, function(user){
					return user.id === Meteor.user()._id;
				});
				if (foundUser !== undefined && foundUser.confirmed === null) { 
					return true;
				}
			}
			return false;
		},
		totalAmount: function() {
			return this.pool.users.length*this.pool.amount;
		},
		participants: function() {
			return _.map(this.pool.users, function(user){
				var userData = Meteor.users.findOne({
					_id : user._id
				});
				return _.merge(user,userData);
			});
		},
		displayStatus : function() {
			if (this.pool.status_id === 0) {
				return 'Opened';
			} else {
				return 'Finished';
			}
		},
		userAlreadyIn: function() {
			var result = _.find(this.pool.users,function(user){
				return user._id == Meteor.user()._id;
			});
			return result;
		},
		timeLeft: function() {
			return moment.duration(moment(this.pool.matchDate).diff(moment())).humanize();
		},
		isPrivate : function() {
			return this.pool.options.is_private ? 'Yes' : 'No';
		}
	});
}
