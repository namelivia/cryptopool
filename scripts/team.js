if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.team.helpers({
		teamName : function () {
			if (this.side === "local"){
				var teamId = Template.parentData().player1;
			} else {
				var teamId = Template.parentData().player2;
			}
			var teamData = Teams.findOne({id : parseInt(teamId)});
			return teamData.name;
		},
		teamLogo : function () {
			if (this.side === "local"){
				var teamId = Template.parentData().player1;
			} else {
				var teamId = Template.parentData().player2;
			}
			var teamData = Teams.findOne({id : parseInt(teamId)});
			return teamData.logo;
		},
	});
}
