"use strict"
if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.team.helpers({
		teamName : function () {
			if (this.side === "local"){
				var teamId = Template.parentData(2).player1;
			} else {
				var teamId = Template.parentData(2).player2;
			}
			var teamData = Teams.findOne({_id : teamId});
			return teamData.name;
		},
		teamLogo : function () {
			if (this.side === "local"){
				var teamId = Template.parentData(2).player1;
			} else {
				var teamId = Template.parentData(2).player2;
			}
			var teamData = Teams.findOne({_id : teamId});
			return 'logos/'+teamData.tag+'.jpg';
		},
	});
}
