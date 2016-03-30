'use strict';
if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.team.helpers({
		teamName : function () {
			return this.team.name;
		},
		teamLogo : function () {
			return '/logos/'+this.team.tag+'.jpg';
		},
	});
}
