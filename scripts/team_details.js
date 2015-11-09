Router.route('/team/:id', function () {
	this.render('teamDetails', {
		data: function () {
			var oid = new Meteor.Collection.ObjectID(this.params.id);
			return Teams.findOne({_id : oid});
		}
	});
},{ 
	name: 'teamDetails',
	waitOn: function() {
		/*var oid = new Meteor.Collection.ObjectID(this.params.id);
		return [
			Meteor.subscribe('teams'),
			Meteor.subscribe('poolsByMatchId',oid),
			Meteor.subscribe('matchById',oid)
		]*/
	}
});

if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.teamDetails.helpers({
		log : function() {
			console.log(this);
			return 'foo';
		}
	});
}
