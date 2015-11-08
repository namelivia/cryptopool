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
			Meteor.call('createPool',amount,this._id);
			event.target.amount.value = "";
			Flash.success("__default__",'Pool successfully created',3000,true);
			Router.go('matchDetails', {id : this._id._str});
		}
	});
	//helpers
}
