'use strict';
if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.matchTextLink.helpers({
		text: function(){
			return this.match.local().name+' - '+this.match.visitant().name;
		}
	});
}
