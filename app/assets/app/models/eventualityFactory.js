/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1, 5] }]*/
/* global integrates, BASE, $xhr, $, Rollbar, angular, secureRandom */
/**
 * @file eventualityFactory.js
 * @author engineering@fluidattacks.com
 */
/**
 * Factory definition for eventuality controler and functions.
 * @name
 * @param {Object} $q
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").factory(
  "eventualityFactory",
  function eventualityFactory ($q) {
    return {

      /**
       * Update an eventuality
       * @function updateEvent
       * @param {Object} eventId Numeric id of the event
       * @param {Object} affectation Value of the affectation
       * @member integrates.eventualityFactory
       * @return {Object} Response of the mutation
       */
      "updateEvent" (eventId, affectation) {
        const oopsAc = "An error ocurred updating event";
        const gQry = `mutation {
          updateEvent(eventId: "${eventId}", affectation: "${affectation}"){
            success
          }
        }`;
        return $xhr.fetch($q, gQry, oopsAc);
      }
    };
  }
);
