'use strict';
if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.match.helpers({
		prettyTime : function() {
			return moment(this.match.date).format("HH:mm");
		},
		prettyDateTime : function() {
			return moment(this.match.date).format("LLLL");
		},
		score1: function(){
			return this.match.score1;
		},
		score2: function(){
			return this.match.score2;
		},
		competitionId: function(){
			return this.match.competition_id;
		},
		local : function(){
			return this.match.local();
		},
		visitant : function(){
			return this.match.visitant();
		},
	});
}
