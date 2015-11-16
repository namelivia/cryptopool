/*
==GENERATE A WALLET, I'M NOT USING THIS ATM==
var keyPair = bitcoinjs.ECKey.makeRandom();
var privKey = keyPair.toWIF();
var pubKey = keyPair.pub.getAddress();
*/
Router.configure({
	layoutTemplate: 'main',
});

if (Meteor.isClient) {
	Session.set("searchDate", new Date());
}

if (Meteor.isServer) {
	Meteor.startup(function () {
		// code to run on server at startup
	});

	Meteor.methods({
		'joinPool': function (poolId,localScore,visitantScore) {
			var pool = Pools.findOne({
				_id: poolId
			});
			if (Meteor.user().tokens >= pool.amount) {
				var userTokensLeft = Meteor.user().tokens - pool.amount;
				var user = {
					'_id' : Meteor.user()._id,
					'localScore' : localScore,
					'visitantScore' : visitantScore,
				}
				Pools.update(
					{ _id: poolId },
					{ $push: { users: user} });
				Meteor.users.update(
					{ _id: Meteor.user()._id },
					{ $set: { tokens: userTokensLeft}, $push: {poolHistory: poolId} });
			} else {
				throw new Meteor.Error('not-enough-tokens', 'Not enough tokens', 'You don\'t have enough tokens to join the pool');
			}
		},
		'createPool': function(amount,matchId){
			var match = Matches.findOne({
				_id: matchId
			});
			if (match.status === 0){
				Pools.insert({
					_id: new Mongo.ObjectID(),
					amount: amount,
					match_id: matchId,
					status_id : 0,
					user_id : Meteor.user()._id,
					users : [],
					createdAt: new Date() // current time
				});
			} else {
				throw new Meteor.Error('match-already-finished', 'Match already finished', 'You can\'t create a pool for a finished match');
			}
		},
		'userExists': function(username){
			return !!Meteor.users.findOne({username : username});
		},
	});

	//Publish the public collections
	Meteor.publish("nextMatches", function () {
		var nextMatches = Matches.find(
			{date : { 
				$gt : new Date()
					}
			},{limit : 5});
		return nextMatches
	});

	Meteor.publish("matchesByDateRange", function (startDate,endDate) {
		return Matches.find(
				{date : { 
							$gte : new Date(startDate),
							$lte : new Date(endDate)
						}
				});
	});

	Meteor.publish("poolsByMatchId", function (matchId) {
		return Pools.find({match_id : matchId});
	});

	Meteor.publish("matchById", function (matchId) {
		return Matches.find({_id : matchId});
	});

	Meteor.publish("teamById", function (teamId) {
		return Teams.find({_id : teamId});
	});

	Meteor.publish("poolById", function (poolId) {
		return Pools.find({_id : poolId});
	});

	Meteor.publish('usersByPoolId', function (poolId) {
		var pool = Pools.findOne({ _id : poolId });
		var userIds = _.map(pool.users,function(user){
			return user._id;
		});
		return Meteor.users.find({ _id: {$in: userIds }},{fields: {'username': 1}});
	});

	Meteor.publish('poolsByUserId', function () {
		var user = Meteor.users.findOne({ _id : this.userId });
		return Pools.find({ _id: {$in: user.poolHistory}});
	});

	Meteor.publish("lastMatches", function () {
		return Matches.find(
			{date : { 
				$lt : new Date()
					}
			},{ limit : 5, sort : { date: -1 }}
		);
	});

	Meteor.publish("teams", function () {
		return Teams.find();
	});

	Meteor.publish("userData", function () {
		return Meteor.users.find({_id: this.userId},
			{fields: {'tokens': 1, 'poolHistory': 1}});
	});

	Accounts.onCreateUser(function(options, user) {
		user.tokens = 10;
		user.poolHistory = [];
		// We still want the default hook's 'profile' behavior.
		if (options.profile) {
			user.profile = options.profile;
		}
		return user;
	});
}
