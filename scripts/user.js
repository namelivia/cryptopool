if (Meteor.isClient) {

	//init
	//events
	//helpers

	Template.user.helpers({
		userId: function(){
			return this._id;
		},
		localScore: function(){
			return this.localScore;
		},
		visitantScore: function(){
			return this.visitantScore;
		}
	});
}
