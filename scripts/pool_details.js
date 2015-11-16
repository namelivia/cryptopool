Router.route('/match/:matchId/pool/:id', function () {
	this.render('poolDetails', {
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
	name: 'poolDetails',
	waitOn: function() {
		var oid = new Meteor.Collection.ObjectID(this.params.id);
		return [
			Meteor.subscribe('poolById',oid),
			Meteor.subscribe('usersByPoolId',oid)
		]
	}
});

if (Meteor.isClient) {
	//init
	//events
	Template.poolDetails.events({
		"click .join": function (event) {
			event.preventDefault();
			Modal.show('confirmJoin',{ _id : this.pool._id })
		}
	});
	//helpers
	Template.poolDetails.helpers({
		userCount : function() {
			return this.pool.users.length;
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
		displaystatus : function() {
			if (this.status === 0) {
				return 'Opened';
			} else {
				return 'finished';
			}
		},
		userAlreadyIn: function() {
			return _.includes(_.map(this.pool.users,function(user){
				return user._id;
			}),Meteor.user()._id);
		},
	});
}
