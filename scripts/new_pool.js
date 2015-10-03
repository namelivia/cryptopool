Router.route('/match/:id/new_pool', function () {
	this.render('newPool', {
	});
},{ name: 'newPool'});

if (Meteor.isClient) {
	//init
	//events
	//helpers
}
