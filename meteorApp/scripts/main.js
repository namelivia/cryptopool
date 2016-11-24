'use strict';
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

var Future; 

if (Meteor.isServer) {
	Meteor.startup(function () {
		// code to run on server at startup
		Future = Npm.require('fibers/future');
	});
	//Configure Twit
	var Twit = new TwitMaker({
		consumer_key: 'XUGsAiaBIqnSoXuRIkE5xNdx5',
		consumer_secret: 'lNFUvR6IOXADfHPtSqqlltE3p6YQVX5qtmvFeAkxiloIuELBdo',
		access_token: '204869812-Ing2mvhNbYnyKMoDSy2Unmz1x6tNFEL0Few4Jcj3',
		access_token_secret: 'oBDpKRYEsClPr86cljZV4pb8DcrgUYrP6GfJwMvZArJFV'
	});

	var insertNotification = function (key,userId,data) {
		Notifications.insert({
			_id: new Mongo.ObjectID(),
			key : key,
			user_id : userId,
			data : data,
			seen : false,
			createdAt: new Date()
		});
	}

	var setUserPoolAccess = function(userId, poolId, access) {
		poolId = new Mongo.ObjectID(poolId);
		var allowedUsers = Pools.findOne({_id : poolId}).allowed_users;
		var index = _.indexOf(
			allowedUsers, _.find(
				allowedUsers, { id :userId }
			)
		);
		allowedUsers.splice(index, 1, { id : allowedUsers[index].id, confirmed:access});
		Pools.update(
			{ _id: poolId },
			{ $set: { allowed_users : allowedUsers } }
		);
		
	}

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
				};
				Pools.update(
					{ _id: poolId },
					{ $push: { users: user} });
				Meteor.users.update(
					{ _id: Meteor.user()._id },
					{ $set: { tokens: userTokensLeft}, $push: {poolHistory: poolId} });
			} else {
				throw new Meteor.Error (
					'not-enough-tokens',
					'Not enough tokens', 
					'You don\'t have enough tokens to join the pool'
				);
			}
		},

		'sendMessage': function(message,userId){
			Messages.insert({
				_id: new Mongo.ObjectID(),
				from: this.userId,
				to: userId,
				message: message,
				createdAt: new Date()
			});
			insertNotification('newMessage',userId,{'from' : this.userId, 'username' : Meteor.user().username});
		},

		'insertNotification': insertNotification,

		'setUserPoolAccess': setUserPoolAccess,

		'allowUserToPool': function(userId, matchId, poolId) {
			setUserPoolAccess(userId, poolId, true);
			insertNotification('accessAllowed',userId,{'from' : this.userId, 'username' : Meteor.user().username,'poolId' : poolId, 'matchId' : matchId});
		},

		'denyUserToPool': function(userId, matchId, poolId) {
			setUserPoolAccess(userId, poolId, false);
			insertNotification('accessDenied',userId,{'from' : this.userId, 'username' : Meteor.user().username,'poolId' : poolId, 'matchId' : matchId});
		},

		'createPool': function(amount,isPrivate,matchId){
			if (isNaN(amount) || amount < 1) {
				throw new Meteor.Error(
					'invalid-token-amount',
					'Invalid token amount',
					'The amount of tokens for the pool is not valid'
				);
			}
			var match = Matches.findOne({
				_id: matchId
			});
			if (match.status === 0){
				Pools.insert({
					_id: new Mongo.ObjectID(),
					amount: amount,
					match_id: matchId,
					is_private: isPrivate,
					status_id : 0,
					user_id : Meteor.user()._id,
					users : [],
					allowed_users : [{'id' : Meteor.user()._id, 'confirmed' : true}],
					matchDate : match.date,
					createdAt: new Date()
				});
			} else {
				throw new Meteor.Error(
					'match-already-finished',
					'Match already finished',
					'You can\'t create a pool for a finished match'
				);
			}
		},
		'requestPoolAccess': function(matchId,poolId){
			var pool = Pools.findOne({_id : poolId});
			Pools.update(
				{ _id: poolId },
				{ $push: { allowed_users: {'id' : Meteor.user()._id ,'confirmed' : undefined}} });
			insertNotification('newAccessRequest',pool.user_id,{'from' : this.userId, 'username' : Meteor.user().username, 'poolId' : poolId._str, 'matchId' : matchId});
		},
		'toggleNotificationAsSeen': function(notificationId){
			notificationId = new Mongo.ObjectID(notificationId);
			var notification = Notifications.findOne({
				_id: notificationId
			});
			Notifications.update(
				{ _id: notificationId },
				{ $set: { seen : !notification.seen } }
			);
		},
		'userExists': function(username){
			return !!Meteor.users.findOne({username : username});
		},
		'getTweets': function(hashtag){
			var fut = new Future();
			Twit.get('search/tweets', {q: hashtag+"-filter:retweets", count: 10},
			function(err, data) {
				fut['return'](data);
			});
			return fut.wait();
		},
	});

	//Publish the public collections
	Meteor.publish("nextMatches", function () {
		var nextMatches = Matches.find(
			{date : { 
				$gt : new Date()
					}
			},{
				limit : 5
			});
		return nextMatches;
	});

	Meteor.publish("myNotifications", function () {
		return Notifications.find(
			{
				user_id : this.userId
			},{sort : {createdAt : -1}}
		);
	});

	Meteor.publish("nextPlayingPoolsByUserId", function () {
		var user = Meteor.users.findOne({ _id : this.userId });
		if (user !== undefined) {
			var nextPools = Pools.find(
				{_id: {$in: user.poolHistory},
				matchDate: { 
					$gte : new Date()
						}
				},{
					limit : 5
				});
			return nextPools;
		}
	});

	Meteor.publish("lastPlayedPoolsByUserId", function () {
		var user = Meteor.users.findOne({ _id : this.userId });
		if (user !== undefined) {
			var lastPools = Pools.find(
				{_id: {$in: user.poolHistory},
				matchDate: { 
					$lte : new Date()
						}
				},{
					limit:5, sort: {
						date:-1
					}
				});
			return lastPools;
		}
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

	Meteor.publish("messagesByUserId", function (userId) {
		return Messages.find( {$or : [
			{to : userId, from: this.userId},
			{to : this.userId, from: userId}
		]});
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

	Meteor.publish('allowedUsersByPoolId', function (poolId) {
		var pool = Pools.findOne({ _id : poolId });
		var userIds = _.map(pool.allowed_users,function(user){
			return user.id;
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

	Meteor.publish("userById", function (userId) {
		var fields = {
			'tokens' : 0,
			'emails' : 0
		}
		if (userId === undefined) {
			userId = this.userId;
			fields.tokens = 1;
			fields.emails = 1;
		}
		return Meteor.users.find(
			{ _id : userId }, {fields : fields}
		);
	});

	Meteor.publish("playersByTeamId", function (teamId) {
		return Players.find({teamId : teamId});
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
