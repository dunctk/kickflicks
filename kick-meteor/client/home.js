Meteor.subscribe("uniquecats");

Template.home.helpers({
  projectsIndex: () => ProjectsIndex,
  uniquecats: function() {
    return UniqueCats.find({});
  }
});

Template.home.events({
  'click .filters': function (e) {
  	var datavalue = $(e.target).attr("data-value");
  	console.log(ProjectsIndex.getComponentMethods(/* optional name */));
  	if (datavalue == "all") { 
  		ProjectsIndex.getComponentMethods().removeProps('categoryFilter');
  	} else {
	    ProjectsIndex.getComponentMethods().addProps('categoryFilter', datavalue);
	}
  },
  'click .navbar-brand': function () {
  	ProjectsIndex.getComponentMethods().removeProps();
  	ProjectsIndex.getComponentMethods().paginate(1);
  	$("#main-search").val("");
  	ProjectsIndex.getComponentMethods().search();
  }
})

Template.home.helpers({
	searchBoxAttributes: function() {
		return{
			class: "form-control",
			id: "main-search",
			placeholder: "Search"
		}
	}
});