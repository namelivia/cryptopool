'use strict';
if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.competition.helpers({
		competitionName : function () {
			return this.competition.name;
		},
		competitionLogo : function () {
			return '/logos/'+this.competition.tag+'.jpg';
		},
	});
}
