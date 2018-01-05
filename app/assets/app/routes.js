/**
 * @file routes.js
 * @author engineering@fluid.la
 */
/**
 * Establece la configuracion de las rutas para integrates
 * @config {AngularJS}
 * @param {Object} $stateProvider
 * @param {Object} $urlRouterProvider
 * @return {undefined}
 */
integrates.config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('home');

    $stateProvider
        .state('home', {
            url: '/home',
            templateUrl: 'assets/views/dashboard.html',
            controller: 'dashboardCtrl'
        })
        .state('ProjectSearch', {
            url: '/project',
            templateUrl: 'assets/views/project/index.html',
            controller: 'projectCtrl'
        })
        .state('ProjectNamed', {
            url: '/project/:project',
            templateUrl: 'assets/views/project/index.html',
            controller: 'projectCtrl'
        })
        .state('FindingDescription', {
            url: '/project/:project/:id/description',
            templateUrl: 'assets/views/project/findingcontent.html',
            controller: 'findingcontentCtrl'
        })
        .state('FindingSeverity', {
            url: '/project/:project/:id/severity',
            templateUrl: 'assets/views/project/findingcontent.html',
            controller: 'findingcontentCtrl'
        })
        .state('FindingTracking', {
            url: '/project/:project/:id/tracking',
            templateUrl: 'assets/views/project/findingcontent.html',
            controller: 'findingcontentCtrl'
        })
        .state('FindingEvidence', {
            url: '/project/:project/:id/evidence',
            templateUrl: 'assets/views/project/findingcontent.html',
            controller: 'findingcontentCtrl'
        })
        .state('FindingExploit', {
            url: '/project/:project/:id/exploit',
            templateUrl: 'assets/views/project/findingcontent.html',
            controller: 'findingcontentCtrl'
        })
        .state('FindingComments', {
            url: '/project/:project/:id/comments',
            templateUrl: 'assets/views/project/findingcontent.html',
            controller: 'findingcontentCtrl'
        })
        .state('EventualitiesByName', {
            url: '/eventualities-by-name',
            templateUrl: 'assets/views/search/event_by_name.html',
            controller: 'eventualityController'
        })
        .state('Forms', {
            url: '/forms',
            templateUrl: '/forms',
            controller: 'formCtrl'
        })
});
integrates.config(function($sceDelegateProvider) {
    $sceDelegateProvider.resourceUrlWhitelist([
      'self',
      '/assets/views/project/eventualityMdl.html',
      'https://fluid.la/**',
    ]);
});
