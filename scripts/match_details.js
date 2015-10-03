Router.route('/match/:id', function () {
	this.render('matchDetails', {
		data: function () {
			return Matches.findOne({id : parseInt(this.params.id)});
		}
	});
},{ name: 'matchDetails'});

if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.matchDetails.helpers({
		prettyDateTime : function() {
			return moment(this.date).format("DD-MM-YYYY HH:mm");
		},
		pools : function(){
			return Pools.find({match_id : this.id});
		}
	});
}
