Router.route('/match/:matchId/pool/:id', function () {
	this.render('poolDetails', {
		data: function () {
			var oid = new Meteor.Collection.ObjectID(this.params.id);
			return Pools.findOne({_id : oid});
		}
	});
},{ name: 'poolDetails'});

if (Meteor.isClient) {
	//init
	//events
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
		}
	});

	Template.poolDetails.events({
		"click .join": function (event) {
			event.preventDefault();
			Modal.show('confirmJoin',{ _id : this._id })
		}
	});
}
