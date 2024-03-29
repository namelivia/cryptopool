Router.route('/calendar', { 
		name: 'calendar',
		template: 'calendar',
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
		"dp.change #datetimepicker" : function (e) {
			var newValue = e.date.toDate();
			var oldValue = Session.get('searchDate');
			if (newValue !== oldValue) {
				Session.set("searchDate", newValue);
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
