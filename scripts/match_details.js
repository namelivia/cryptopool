Router.route('/match/:id', function () {
	this.render('matchDetails', {
		waitOn: function(){
			return [
				Meteor.suscribe("oneMatch",this.params.id)
			];
		},
		data: function () {
			return Matches.findOne({id : this.params.id});
		},
		action : function () {	
			if (this.ready()) {
				console.log('ready');
				this.render();
			}
		}
	});
},{ name: 'matchDetails'});

if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.matchDetails.helpers({
		prettyDateTime : function() {
			console.log('data:');
			console.log(this);
			return 'log';
		}
	});
}
