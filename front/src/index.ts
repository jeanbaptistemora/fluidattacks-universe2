/* eslint-disable angular/file-name */
/**
 * @file index.ts
 * @description Controllers integrator for Integrates
 */
import angular from "angular";
import { react2angular } from "react2angular";
import frame from "./components/Frame/index";
import preloader from "./components/Preloader/index";
import indicatorBox from "./scenes/Dashboard/components/IndicatorBox/index";
import indicatorGraph from "./scenes/Dashboard/components/IndicatorGraph/index";
import Access from "./scenes/Login/components/Access/index";
import compulsoryNotice from "./scenes/Registration/components/CompulsoryNotice/index";

/**
 * @url: /index
 * @page: index.html
 * @controllers: undefined
 * @tag: <login/>
 */
angular
  .module("FluidIntegrates")
  .component(
    "login",
    react2angular(
      Access,
      [],
    ),
  );

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
/**
 * @url: /registration
 * @page: registration.html
 * @controllers: ["registerCtrl"]
 * @tag: <compulsory-notice/>
 */
angular
  .module("FluidIntegrates")
  .component(
    "compulsoryNotice",
    react2angular(
      compulsoryNotice,
      [
        "btnAcceptText",
        "btnAcceptTooltip",
        "id",
        "onAccept",
        "rememberText",
        "rememberTooltip",
        "noticeText",
        "noticeTitle",
      ],
    ),
  );
/**
 * @url: #/project/:name/indicators
 * @page: indicators.html
 * @controllers: ["projectIndicatorsCtrl"]
 * @tag: <frame/>
 */
angular
  .module("FluidIntegrates")
  .component(
    "formFrame",
    react2angular(
      frame,
      [
        "id",
        "src",
        "height",
      ],
    ),
  );

  /**
   * @url: #/
   * @page: *
   * @controllers: []
   * @tag: <preloader/>
   */
angular
  .module("FluidIntegrates")
  .component(
    "preloader",
    react2angular(
      preloader,
      [],
    ),
  );
