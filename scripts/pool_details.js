Router.route('/match/:matchId/pool/:id', function () {
	this.render('poolDetails', {
		data: function () {
			var oid = new Meteor.Collection.ObjectID(this.params.id);
			return Pools.findOne({_id : oid});
		}
	});
},{ 
	name: 'poolDetails',
	waitOn: function() {
		var oid = new Meteor.Collection.ObjectID(this.params.id);
		return [
			Meteor.subscribe('poolById',oid)
		]
	}
});

if (Meteor.isClient) {
	//init
	//events
	Template.poolDetails.events({
		"click .join": function (event) {
			event.preventDefault();
			Modal.show('confirmJoin',{ _id : this._id })
		}
	});
	//helpers
	Template.poolDetails.helpers({
		userCount : function() {
			return this.users.length;
		},
		totalAmount: function() {
			return this.users.length*this.amount;
		},
		participants: function() {
			return this.users;
		},
		userAlreadyIn: function() {
			return _.includes(_.map(this.users,function(user){
				return user._id;
			}),Meteor.user()._id);
		},
	});
}
