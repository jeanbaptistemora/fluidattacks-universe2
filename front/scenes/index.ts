/* eslint-disable angular/file-name */
/**
 * @file index.ts
 * @description Controllers integrator for Integrates
 */
import angular from "angular";
import { react2angular } from "react2angular";
import formController from "./controller/form.controller";
import indicatorBox from "./Dashboard/components/IndicatorBox/index";
import indicatorGraph from "./Dashboard/components/IndicatorGraph/index";
angular.module("FluidIntegrates")
  .controller("formController", formController);
/**
 * @url: #/project/:name/indicators
 * @page: indicators.html
 * @controllers: ["projectIndicatorsCtrl"]
 * @tag: <indicator-box/>
 */
angular
  .module("FluidIntegrates")
  .component(
    "indicatorBox",
    react2angular(
      indicatorBox,
      [
        "backgroundColor",
        "color",
        "icon",
        "name",
        "quantity",
        "title",
      ],
    ),
  );
/**
 * @url: #/project/:name/indicators
 * @page: indicators.html
 * @controllers: ["projectIndicatorsCtrl"]
 * @tag: <indicator-graph/>
 */
angular
  .module("FluidIntegrates")
  .component(
    "indicatorGraph",
    react2angular(
      indicatorGraph,
      [
        "data",
        "name",
      ],
    ),
  );
