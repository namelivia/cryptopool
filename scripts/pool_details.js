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
		}
	});
}
