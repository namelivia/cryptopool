Router.route('/match/:id/new_pool', function () {
	this.render('newPool', {
		data: function () {
			var oid = new Meteor.Collection.ObjectID(this.params.id);
			return Matches.findOne({_id : oid});
		}
	});
},{ name: 'newPool'});

if (Meteor.isClient) {
	//init
	//events
	Template.newPool.events({
		"submit .new-pool": function (event) {
			event.preventDefault();
			var amount = parseInt(event.target.amount.value);

			Pools.insert({
				_id: new Mongo.ObjectID(),
				amount: amount,
				match_id: this._id,
				status_id : 3,
				users : [],
				createdAt: new Date() // current time
			});
			
			Flash.success('Pool successfully created');
			event.target.amount.value = "";
		}
	});
	//helpers
}
