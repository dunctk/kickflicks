Template.admin_cron.events({
	'click #run-import': function (evt, template) {
		Meteor.call("getNewProjects");
	}
});