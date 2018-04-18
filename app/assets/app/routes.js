/* globals integrates, BASE,  $ */


/**
 * @file routes.js
 * @author engineering@fluidattacks.com
 */
/**
 * Establece la configuracion de las rutas para integrates
 * @config {AngularJS}
 * @param {Object} $stateProvider
 * @param {Object} $urlRouterProvider
 * @return {undefined}
 */
/** @export */
integrates.config(function config ($stateProvider, $urlRouterProvider) {
  $urlRouterProvider.otherwise("home");

  $stateProvider.
    state("home", {
      "controller": "dashboardCtrl",
      "templateUrl": "assets/views/dashboard.html",
      "url": "/home"
    }).
    state("ProjectSearch", {
      "controller": "projectCtrl",
      "templateUrl": "assets/views/project/index.html",
      "url": "/project"
    }).
    state("ProjectNamed", {
      "controller": "projectCtrl",
      "templateUrl": "assets/views/project/index.html",
      "url": "/project/:project"
    }).
    state("ProjectIndicators", {
      "controller": "projectIndicatorsCtrl",
      "templateUrl": `${BASE.url}project_indicators`,
      "url": "/project/:project/indicators"
    }).
    state("ProjectFindings", {
      "controller": "projectFindingsCtrl",
      "templateUrl": `${BASE.url}project_findings?l=${localStorage.lang}`,
      "url": "/project/:project/findings"
    }).
    state("ProjectEvents", {
      "controller": "projectEventsCtrl",
      "templateUrl": `${BASE.url}project_events?l=${localStorage.lang}`,
      "url": "/project/:project/events"
    }).
    state("FindingDescription", {
      "controller": "findingcontentCtrl",
      "templateUrl": "assets/views/project/findingcontent.html",
      "url": "/project/:project/:id/description"
    }).
    state("FindingSeverity", {
      "controller": "findingcontentCtrl",
      "templateUrl": "assets/views/project/findingcontent.html",
      "url": "/project/:project/:id/severity"
    }).
    state("FindingTracking", {
      "controller": "findingcontentCtrl",
      "templateUrl": "assets/views/project/findingcontent.html",
      "url": "/project/:project/:id/tracking"
    }).
    state("FindingEvidence", {
      "controller": "findingcontentCtrl",
      "templateUrl": "assets/views/project/findingcontent.html",
      "url": "/project/:project/:id/evidence"
    }).
    state("FindingExploit", {
      "controller": "findingcontentCtrl",
      "templateUrl": "assets/views/project/findingcontent.html",
      "url": "/project/:project/:id/exploit"
    }).
    state("FindingRecords", {
      "controller": "findingcontentCtrl",
      "templateUrl": "assets/views/project/findingcontent.html",
      "url": "/project/:project/:id/records"
    }).
    state("FindingComments", {
      "controller": "findingcontentCtrl",
      "templateUrl": "assets/views/project/findingcontent.html",
      "url": "/project/:project/:id/comments"
    }).
    state("Forms", {
      "controller": "formCtrl",
      "templateUrl": `${BASE.url}forms`,
      "url": "/forms"
    });
});
integrates.config(function config ($sceDelegateProvider) {
  $sceDelegateProvider.resourceUrlWhitelist([
    "self",
    "/assets/views/project/eventualityMdl.html",
    "https://fluidattacks.com/**"
  ]);
});
