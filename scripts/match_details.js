Router.route('/match/:id', function () {
	this.render('matchDetails', {
		data: function () {
			var oid = new Meteor.Collection.ObjectID(this.params.id);
			return Matches.findOne({_id : oid});
		}
	});
},{ 
	name: 'matchDetails',
	waitOn: function() {
		var oid = new Meteor.Collection.ObjectID(this.params.id);
		return [
			Meteor.subscribe('teams'),
			Meteor.subscribe('poolsByMatchId',oid),
			Meteor.subscribe('matchById',oid)
		]
	}
});

if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.matchDetails.helpers({
		prettyDateTime : function() {
			return moment(this.date).format("DD-MM-YYYY HH:mm");
		},
		pools : function(){
			return this.pools();
		},
		local : function(){
			return this.local();
		},
		visitant : function(){
			return this.visitant();
		}
	});
}
