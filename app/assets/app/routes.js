// This file is an Angular configuration script for Integrates services
/* eslint-disable angular/component-limit*/
/* globals integrates, BASE, angular, $ */

/**
 * @file routes.js
 * @author engineering@fluidattacks.com
 */
/**
 * Configuration for Integrates routes.
 * @config {AngularJS}
 * @param {Object} $stateProvider
 * @param {Object} $urlRouterProvider
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").config((
  $stateProvider,
  $urlRouterProvider
) => {
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
    state("ProjectDrafts", {
      "controller": "projectDraftsCtrl",
      "templateUrl": `${BASE.url}project_drafts?l=${localStorage.lang}`,
      "url": "/project/:project/drafts"
    }).
    state("ProjectEvents", {
      "controller": "projectEventsCtrl",
      "templateUrl": `${BASE.url}project_events?l=${localStorage.lang}`,
      "url": "/project/:project/events"
    }).
    state("ProjectResources", {
      "controller": "projectResourcesCtrl",
      "templateUrl": `${BASE.url}project_resources?l=${localStorage.lang}`,
      "url": "/project/:project/resources"
    }).
    state("ProjectUsers", {
      "controller": "projectUsersCtrl",
      "templateUrl": `${BASE.url}project_users?l=${localStorage.lang}`,
      "url": "/project/:project/users"
    }).
    state("EventsDescription", {
      "controller": "eventContentCtrl",
      "templateUrl": "assets/views/project/eventcontent.html",
      "url": "/project/:project/events/:id/description"
    }).
    state("EventsEvidence", {
      "controller": "eventContentCtrl",
      "templateUrl": "assets/views/project/eventcontent.html",
      "url": "/project/:project/events/:id/evidence"
    }).
    state("FindingDescription", {
      "controller": "findingContentCtrl",
      "templateUrl": "assets/views/project/findingcontent.html",
      "url": "/project/:project/:id/description"
    }).
    state("FindingSeverity", {
      "controller": "findingContentCtrl",
      "templateUrl": "assets/views/project/findingcontent.html",
      "url": "/project/:project/:id/severity"
    }).
    state("FindingTracking", {
      "controller": "findingContentCtrl",
      "templateUrl": "assets/views/project/findingcontent.html",
      "url": "/project/:project/:id/tracking"
    }).
    state("FindingEvidence", {
      "controller": "findingContentCtrl",
      "templateUrl": "assets/views/project/findingcontent.html",
      "url": "/project/:project/:id/evidence"
    }).
    state("FindingExploit", {
      "controller": "findingContentCtrl",
      "templateUrl": "assets/views/project/findingcontent.html",
      "url": "/project/:project/:id/exploit"
    }).
    state("FindingRecords", {
      "controller": "findingContentCtrl",
      "templateUrl": "assets/views/project/findingcontent.html",
      "url": "/project/:project/:id/records"
    }).
    state("FindingComments", {
      "controller": "findingContentCtrl",
      "templateUrl": "assets/views/project/findingcontent.html",
      "url": "/project/:project/:id/comments"
    }).
    state("FindingObservations", {
      "controller": "findingContentCtrl",
      "templateUrl": "assets/views/project/findingcontent.html",
      "url": "/project/:project/:id/observations"
    }).
    state("Forms", {
      "controller": "formController",
      "templateUrl": `${BASE.url}forms`,
      "url": "/forms"
    });
});
angular.module("FluidIntegrates").config(($sceDelegateProvider) => {
  $sceDelegateProvider.resourceUrlWhitelist([
    "self",
    "/assets/views/project/eventualityMdl.html",
    "https://fluidattacks.com/**"
  ]);
});
