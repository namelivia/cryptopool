'use strict';
Router.route('/team/:id', function () {
	this.render('teamDetails', {
		data: function () {
			var oid = new Meteor.Collection.ObjectID(this.params.id);
			return Teams.findOne({_id : oid});
		}
	});
},{ 
	name: 'teamDetails',
	waitOn: function() {
		var oid = new Meteor.Collection.ObjectID(this.params.id);
		return [
			Meteor.subscribe('teamById',oid),
			Meteor.subscribe('playersByTeamId',oid),
		];
	},
	onBeforeAction: function() {
		if (!Meteor.user()) {
			this.render('landing');
		}
		else {
			this.next();
		}
	}
});

if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.teamDetails.helpers({
		teamLogo : function () {
			return '/logos/'+this.tag+'.jpg';
		},
		players : function(){
			return this.players();
		},
	});
}