Router.route('/match/:matchId/pool/:id', function () {
	this.render('poolDetails', {
		/*
		data: function () {
			return Matches.findOne({id : parseInt(this.params.id)});
		}*/
	});
},{ name: 'poolDetails'});

if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.poolDetails.helpers({
	});
}
