Matches = new Mongo.Collection('matches');
Teams = new Mongo.Collection('teams');
Matches.helpers({
	local: function() {
		return Teams.findOne({ _id: this.player1 });
	},
	visitant: function() {
		return Teams.findOne({ _id: this.player2 });
	},
});
