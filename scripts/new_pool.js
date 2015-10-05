Router.route('/match/:id/new_pool', function () {
	this.render('newPool', {
		data: function () {
			return Matches.findOne({id : parseInt(this.params.id)});
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
				amount: amount,
				match_id: this.id,
				status_id : 3,
				users : [],
				createdAt: new Date() // current time
			});

			event.target.amount.value = "";
		}
	});
	//helpers
}
