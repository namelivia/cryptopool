Router.route('/match/:id', function () {
	this.render('matchDetails', {
		data: function () {
			var oid = new Meteor.Collection.ObjectID(this.params.id);
			return Matches.findOne({_id : oid});
		}
	});
},{ 
	name: 'matchDetails',
	waitOn: function() {
		var oid = new Meteor.Collection.ObjectID(this.params.id);
		return [
			Meteor.subscribe('teams'),
			Meteor.subscribe('poolsByMatchId',oid),
			Meteor.subscribe('matchById',oid)
		]
	}
});

if (Meteor.isClient) {
	//init
	Template.matchDetails.created = function() {
		var self = this;
		self.tweets = new ReactiveVar([]);
		Meteor.call('getTweets',Template.currentData().hashtag,function(error,result){
			self.tweets.set(result.statuses);
		});
	}
	//events
	Template.matchDetails.events({
		"click .new_pool": function (event) {
			event.preventDefault();
			Modal.show('newPool',{ matchId : this._id})
		}
	});
	//helpers
	Template.matchDetails.helpers({
		prettyDateTime : function() {
			return moment(this.date).format("DD-MM-YYYY HH:mm");
		},
		displayStatus : function() {
			if (this.status === 0) {
				return 'To be played';
			} else {
				return 'Finished';
			}
		},
		newPoolsAllowed : function() {
			return this.status === 0;
		},
		pools : function(){
			return this.pools();
		},
		local : function(){
			return this.local();
		},
		visitant : function(){
			return this.visitant();
		},
		tweets: function(){
			return Template.instance().tweets.get();
		}
	});
}
