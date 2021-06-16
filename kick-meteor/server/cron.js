SyncedCron.start()

SyncedCron.add({

  name: "get new kickstarter projects from shub",

  schedule: function(parser){
    return parser.recur().on('08:00:00').time();
  },

  job: function(){
    return Meteor.call("getNewProjects");
  }
});

Meteor.methods({
	getNewProjects: function () {
	  	var shubApiKey = "28ea6daa403e4b0aabeae252748bdb14";
	    var result = Meteor.http.call("GET", "https://storage.scrapinghub.com/items/36617/1/25", 
	    							{auth: "28ea6daa403e4b0aabeae252748bdb14:"});
	    var data = result['content'];
	    data = data.replace(/(\r\n|\n|\r)/gm,"");
	    data = data.replace(/\}\{/gm,"},{");
	    data = "[" + data + "]";
	    data = JSON.parse(data);

		var added = 0;
		var duplicates = 0;
		for (var n = 0; n < data.length; n++) {
			var project = data[n];

			try {
	    		KickstarterProjects.insert({
	    			name : project.name,
					shortDesc : project.shortDesc,
					image : project.image,
					video : project.video,
					fundGoal : Math.round(project.fundGoal),
					fundReached : Math.round(project.fundReached),
					fundPercent : Math.round(project.fundPercent * 100),
					inverseFundPercent : Math.round(project.fundGoal / project.fundReached),
					backersCount : project.backersCount,
					creatorName : project.creatorName,
					creatorProfileUrl : project.creatorProfileUrl,
					creatorProfileImage : project.creatorProfileImage,
					launchDate : project.launchDate,
					category : project.category,
					subcategory : project.subcategory,
					pageUrl : project.pageUrl
	    		});
	    		added++;
			} catch(e) {
				duplicates++;
			}
		};
		console.log(added + " added and " + duplicates + " duplicates ignored");

  }  
});




