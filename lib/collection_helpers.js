Matches = new Mongo.Collection('matches');
Teams = new Mongo.Collection('teams');
Pools = new Mongo.Collection('pools');
Matches.helpers({
	local: function() {
		return Teams.findOne({ _id: this.player1 });
	},
	visitant: function() {
		return Teams.findOne({ _id: this.player2 });
	},
	pools: function() {
		return Pools.find({match_id : this._id});
	}
});
