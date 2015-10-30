Router.route('/calendar', { 
	name: 'calendar',
	template: 'calendar',
	waitOn: function() {
		return [
			Meteor.subscribe('teams')
		]
	},
	onBeforeAction: function() {
		this.next();
	}
});

if (Meteor.isClient) {

	//init

	Template.calendar.onRendered(function() {
		    this.$('.date').datetimepicker({
				format: 'DD-MM-YYYY',
				defaultDate: Session.get('searchDate')
			});
	});

	//events

	Template.calendar.events({
		"dp.change #datetimepicker" : function (event,template) {
			var newValue = event.date.toDate();
			var oldValue = Session.get('searchDate');
			if (newValue !== oldValue) {
				Session.set("searchDate", newValue);
				//TODO: I would like to set this just once in the template
				startDate = Session.get('searchDate').setHours(0,0,0,0);
				endDate = Session.get('searchDate').setHours(23,59,59,999);
				Meteor.subscribe('matchesByDateRange',startDate,endDate);
			}
		}
	});

	//helpers

	Template.calendar.helpers({
		searchDate : function (){
			var date = Session.get('searchDate');
			return moment(date).format('DD-MM-YYYY');
		},
		matches : function(){
			var startDate = Session.get('searchDate').setHours(0,0,0,0);
			var endDate = Session.get('searchDate').setHours(23,59,59,999);
			return Matches.find(
					{date : { 
								$gte : new Date(startDate),
								$lte : new Date(endDate)
							}
					});
		}
	});
}
