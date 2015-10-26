if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.match.helpers({
		prettyTime : function() {
			return moment(Template.parentData(1).date).format("HH:mm");
		},
		prettyDateTime : function() {
			return moment(Template.parentData(1).date).format("DD-MM-YYYY HH:mm");
		}
	});
}
