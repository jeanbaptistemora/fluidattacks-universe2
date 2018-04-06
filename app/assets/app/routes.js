/* globals integrates, BASE,  $ */
"use strict";

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
integrates.config(function ($stateProvider, $urlRouterProvider) {
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
    state("EventualitiesByName", {
      "controller": "eventualityController",
      "templateUrl": "assets/views/search/event_by_name.html",
      "url": "/eventualities-by-name"
    }).
    state("Forms", {
      "controller": "formCtrl",
      "templateUrl": `${BASE.url}forms`,
      "url": "/forms"
    });
});
integrates.config(function ($sceDelegateProvider) {
  $sceDelegateProvider.resourceUrlWhitelist([
    "self",
    "/assets/views/project/eventualityMdl.html",
    "https://fluidattacks.com/**"
  ]);
});
