Matches = new Mongo.Collection('matches');
Teams = new Mongo.Collection('teams');
Pools = new Mongo.Collection('pools');
Players = new Mongo.Collection('players');
Notifications = new Mongo.Collection('notifications');
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
Teams.helpers({
	players: function(){
		return Players.find({teamId : this._id});
	}
});
Pools.helpers({
	match: function(){
		return Matches.findOne({_id : this.match_id});
	}
});
