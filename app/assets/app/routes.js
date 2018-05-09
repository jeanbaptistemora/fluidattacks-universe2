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
    state("ProjectReleases", {
      "controller": "projectReleasesCtrl",
      "templateUrl": `${BASE.url}project_releases?l=${localStorage.lang}`,
      "url": "/project/:project/releases"
    }).
    state("ProjectEvents", {
      "controller": "projectEventsCtrl",
      "templateUrl": `${BASE.url}project_events?l=${localStorage.lang}`,
      "url": "/project/:project/events"
    }).
    state("ProjectUsers", {
      "controller": "projectUsersCtrl",
      "templateUrl": `${BASE.url}project_users?l=${localStorage.lang}`,
      "url": "/project/:project/users"
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
    state("ReleaseDescription", {
      "controller": "releaseContentCtrl",
      "templateUrl": "assets/views/project/releasecontent.html",
      "url": "/project/:project/release/:id/description"
    }).
    state("ReleaseSeverity", {
      "controller": "releaseContentCtrl",
      "templateUrl": "assets/views/project/releasecontent.html",
      "url": "/project/:project/release/:id/severity"
    }).
    state("ReleaseEvidence", {
      "controller": "releaseContentCtrl",
      "templateUrl": "assets/views/project/releasecontent.html",
      "url": "/project/:project/release/:id/evidence"
    }).
    state("ReleaseExploit", {
      "controller": "releaseContentCtrl",
      "templateUrl": "assets/views/project/releasecontent.html",
      "url": "/project/:project/release/:id/exploit"
    }).
    state("ReleaseRecords", {
      "controller": "releaseContentCtrl",
      "templateUrl": "assets/views/project/releasecontent.html",
      "url": "/project/:project/release/:id/records"
    }).
    state("Forms", {
      "controller": "formCtrl",
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
