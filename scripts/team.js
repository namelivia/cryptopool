"use strict"
if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.team.helpers({
		teamName : function () {
			var teamData = Teams.findOne({_id : this.teamId});
			return teamData.name;
		},
		teamLogo : function () {
			var teamData = Teams.findOne({_id : this.teamId});
			return 'logos/'+teamData.tag+'.jpg';
		},
	});
}
