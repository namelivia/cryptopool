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
			Meteor.subscribe('teamById',oid)
		]
	}
});

if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.teamDetails.helpers({
		teamName : function() {
			return this.name;
		},
		teamLogo : function () {
			return '/logos/'+this.tag+'.jpg';
		},
	});
}
