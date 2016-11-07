'use strict';
Router.route('/conversation/:id', function () {
	this.render('conversation', {
		data: function () {
			return { userId : this.params.id }
		}
	});
},{ 
	name: 'conversation',
	waitOn: function() {
		return [
			Meteor.subscribe('messagesByUserId',this.params.id),
			Meteor.subscribe('userById',this.params.id)
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
	Template.conversation.events({
		'submit .new-message': function (event) {
			event.preventDefault();
			var message = event.target.newMessage.value;
			event.target.newMessage.value = '';
			Meteor.call('sendMessage',message, this.userId,function(error,response){
				if (error){
					toastr.error(error.details, error.reason);
				} else {
					toastr.success('You have sent a message to this user', 'Message sent');
				}
			});
		}
	});
	//helpers
	Template.conversation.helpers({
		messages: function() {
			return Messages.find({});
		},
		hasMessages: function() {
			return Messages.find({}).count() > 0;
		},
	});
}
