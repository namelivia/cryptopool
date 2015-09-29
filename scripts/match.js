Router.route('/match/:id', function () {
	this.render('matchDetails', {
		data: function () {
			return Matches.findOne({ id: parseInt(this.params.id)});
		}
	});
},{ name: 'matchDetails'});

if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.match.helpers({
		prettyTime : function() {
			return moment(this.date).format("HH:mm");
		},
		prettyDateTime : function() {
			return moment(this.date).format("DD-MM-YYYY HH:mm");
		},
		upcomingMatchesContext: function() {
			return this.context === "upcomingMatches";
		}
	});
}
