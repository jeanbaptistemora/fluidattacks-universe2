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
    state("home", {"url": "/home"}).
    state("ProjectIndicators", {"url": "/project/:project/indicators"}).
    state("ProjectFindings", {"url": "/project/:project/findings"}).
    state("ProjectDrafts", {"url": "/project/:project/drafts"}).
    state("ProjectEvents", {"url": "/project/:project/events"}).
    state("ProjectResources", {"url": "/project/:project/resources"}).
    state("ProjectUsers", {"url": "/project/:project/users"}).
    state("ProjectComments", {"url": "/project/:project/comments"}).
    state("EventsDescription", {"url": "/project/:project/events/:id/description"}).
    state("EventsEvidence", {"url": "/project/:project/events/:id/evidence"}).
    state("FindingDescription", {"url": "/project/:project/:id/description"}).
    state("FindingSeverity", {"url": "/project/:project/:id/severity"}).
    state("FindingTracking", {"url": "/project/:project/:id/tracking"}).
    state("FindingEvidence", {"url": "/project/:project/:id/evidence"}).
    state("FindingExploit", {"url": "/project/:project/:id/exploit"}).
    state("FindingRecords", {"url": "/project/:project/:id/records"}).
    state("FindingComments", {"url": "/project/:project/:id/comments"}).
    state("FindingObservations", {"url": "/project/:project/:id/observations"}).
    state("Forms", {"url": "/forms"});
});

angular.module("FluidIntegrates").config(($sceDelegateProvider) => {
  $sceDelegateProvider.resourceUrlWhitelist([
    "self",
    "https://fluidattacks.com/**"
  ]);
});
