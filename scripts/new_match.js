if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.newMatch.events({
		"submit .new-match": function (event) {
			event.preventDefault();
			var player1 = parseInt(event.target.localTeam.value);
			var player2 = parseInt(event.target.visitantTeam.value);
			var score1 = parseInt(event.target.score1.value);
			var score2 = parseInt(event.target.score2.value);

			Matches.insert({
				player1: player1,
				player2: player2,
				score1: score1,
				score2: score2,
				createdAt: new Date() // current time
			});

			event.target.localTeam.value = "";
			event.target.visitantTeam.value = "";
			event.target.score1.value = "";
			event.target.score2.value = "";
		}
	});
}
