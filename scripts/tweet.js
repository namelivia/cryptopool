if (Meteor.isClient) {
	//init
	//events
	//helpers
	Template.tweet.helpers({
		tweetPhoto: function() {
			var imageString = '<a href="https://twitter.com/'+
				this.user.screen_name+'"><img src="'+this.user.profile_image_url+'"></img></a>';
			return new Handlebars.SafeString(imageString);
		},
		tweetContent: function() {
			var replaceIndex = [];
			var append = []
			_.forEach(this.entities,function(value,key){
				var prefix = '';
				var display = false;
				var find = '';
				var url = null;
				var size = null;
				switch (key) {
					case 'hashtags':
						find = 'text';
						prefix = '#';
						url = 'https://twitter.com/search/?src=hash&q=%23';
						break;
					case 'user_mentions':
						find = 'screen_name';
						prefix = '@';
						url = 'https://twitter.com/';
						break;
					/*
					case 'media':
						display = 'media_url_https';
						href = 'media_url_https';
						size = 'small';
						break;
					*/
					case 'urls':
						find = 'url';
						display = 'display_url';
						url = 'expanded_url';
						break;
					default:
						break;
				}
				_.forEach(value,function(item){
					if (key !== 'media') {
						var replace = prefix+item[find];
						var href = 'url' in item ? item[url] : url; 
						if (href.search('http') === -1) {
							href = 'http://'+href;
						}
						if (prefix.length > 0) {
							href += item[find];
						}
						var withString = '<a href="'+href+'">'+replace+'</a>'; 
						var replaceObj = {};
						replaceObj.orig = replace;
						replaceObj.dest = withString;
						replaceIndex.push(replaceObj);
					}
				});
			});
			var replacedText = this.text;
			for (j=0;j<replaceIndex.length;j++) {
				replacedText = replacedText.replace(replaceIndex[j].orig,replaceIndex[j].dest);
			}
			//Only If im displaying images
			//foreach ($append as $add) $tweet['text'] .= $add;
			var createdAt = moment(this.created_at);
			var tweetInfo = '<a href="https://twitter.com/'+
				this.user.screen_name+'">'+this.user.name+
				'</a> @'+this.user.screen_name+' &#183; '+
				'<a href="http://twitter.com/'+this.user.screen_name+
				'/status/'+this.id+'">'+createdAt.fromNow()+'</a><br />';
			return new Handlebars.SafeString(tweetInfo+replacedText);
		}
	});
}
