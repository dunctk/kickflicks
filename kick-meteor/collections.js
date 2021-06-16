KickstarterProjects = new Mongo.Collection('kickstarterprojects'),
	ProjectsIndex = new EasySearch.Index({
		collection: KickstarterProjects,
		fields: ['name', 'description'],
		engine: new EasySearch.MongoDB({
			sort: function () {
		      return { launchDate: -1 };
		    },
		    selector: function (searchObject, options, aggregation) {
		      let selector = this.defaultConfiguration().selector(searchObject, options, aggregation),
		        categoryFilter = options.search.props.categoryFilter;

		      if (_.isString(categoryFilter) && !_.isEmpty(categoryFilter)) {
		        selector.subcategory = categoryFilter;
		      }

		      return selector;
		    }
		}),
		defaultSearchOptions: {
			limit: 6
		}
	});

UniqueCats = new Mongo.Collection('uniquecats');

if (Meteor.isServer) {
	KickstarterProjects._ensureIndex({pageUrl: 1}, {unique: 1});
	UniqueCats.upsert(
		{
			_id: "dEExcGKytQfiGSmW6"
		},
		{
			categories: KickstarterProjects.distinct("category"),
			subcategories: KickstarterProjects.distinct("subcategory")
		}
	);
 
	Meteor.publish("uniquecats", function() {
		return UniqueCats.find();
	});
}