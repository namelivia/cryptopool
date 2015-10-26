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
		return [
			Meteor.subscribe('teams')
		]
	},
	onBeforeAction: function() {
		this.next();
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
			return Pools.find({match_id : this._id});
		}
	});
}
