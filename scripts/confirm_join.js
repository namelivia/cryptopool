if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.confirmJoin.events({
		"click .confirm": function (event) {
			event.preventDefault();
			Modal.show('confirmJoin')
			Pools.update(
				{ _id: this._id },
				{ $push: { users: Meteor.user()._id } }
			);
			var key = bitcoinjs.ECKey.makeRandom();
			console.log(key.toWIF());    
			console.log(key.pub.getAddress().toString());
			Flash.success("__default__",'You have joined the pool',3000,true);
		}
	});
}
