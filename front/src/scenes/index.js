"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
/* eslint-disable angular/file-name */
/**
 * @file index.ts
 * @description Controllers integrator for Integrates
 */
var angular_1 = __importDefault(require("angular"));
var react2angular_1 = require("react2angular");
var index_1 = __importDefault(require("./components/Frame/index"));
var index_2 = __importDefault(require("./Dashboard/components/IndicatorBox/index"));
var index_3 = __importDefault(require("./Dashboard/components/IndicatorGraph/index"));
var index_4 = __importDefault(require("./Registration/components/LegalNotice/index"));
/**
 * @url: #/project/:name/indicators
 * @page: indicators.html
 * @controllers: ["projectIndicatorsCtrl"]
 * @tag: <indicator-box/>
 */
angular_1.default
    .module("FluidIntegrates")
    .component("indicatorBox", react2angular_1.react2angular(index_2.default, [
    "backgroundColor",
    "color",
    "icon",
    "name",
    "quantity",
    "title",
]));
/**
 * @url: #/project/:name/indicators
 * @page: indicators.html
 * @controllers: ["projectIndicatorsCtrl"]
 * @tag: <indicator-graph/>
 */
angular_1.default
    .module("FluidIntegrates")
    .component("indicatorGraph", react2angular_1.react2angular(index_3.default, [
    "data",
    "name",
]));
/**
 * @url: /registration
 * @page: registration.html
 * @controllers: ["registerCtrl"]
 * @tag: <legal-notice/>
 */
angular_1.default
    .module("FluidIntegrates")
    .component("legalNotice", react2angular_1.react2angular(index_4.default, [
    "btnAcceptText",
    "id",
    "onClick",
    "rememberText",
    "text",
    "title",
]));
/**
 * @url: #/project/:name/indicators
 * @page: indicators.html
 * @controllers: ["projectIndicatorsCtrl"]
 * @tag: <frame/>
 */
angular_1.default
    .module("FluidIntegrates")
    .component("formFrame", react2angular_1.react2angular(index_1.default, [
    "id",
    "src",
    "height",
]));
