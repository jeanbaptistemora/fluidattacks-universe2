// This file should not be renamed
/* eslint-disable angular/file-name */
/**
 * @file index.ts
 * @description Controllers integrator for Integrates
 */
import angular from "angular";
import formCtrl from "./controller/form.controller";

angular.module("FluidIntegrates").controller(
  "formCtrl",
  formCtrl
);
