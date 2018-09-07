/* eslint-disable angular/file-name */
/**
 * @file index.ts
 * @description Controllers integrator for Integrates
 */
import angular from "angular";
import { react2angular } from "react2angular";
import dataTable from "./components/DataTable/index";
import frame from "./components/Frame/index";
import preloader from "./components/Preloader/index";
import commentBox from "./scenes/Dashboard/components/CommentBox/index";
import exploitView from "./scenes/Dashboard/components/ExploitView/index";
import fieldBox from "./scenes/Dashboard/components/FieldBox/index";
import imageGallery from "./scenes/Dashboard/components/ImageGallery/index";
import indicatorBox from "./scenes/Dashboard/components/IndicatorBox/index";
import indicatorGraph from "./scenes/Dashboard/components/IndicatorGraph/index";
import { trackingView } from "./scenes/Dashboard/components/TrackingView/index";
import Access from "./scenes/Login/components/Access/index";
import { compulsoryNotice } from "./scenes/Registration/components/CompulsoryNotice/index";

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
 * @url: #/project/:project/events/:id/description
 * @page: eventcontent.html
 * @controllers: ["eventContentCtrl"]
 * @tag: <field-box/>
 */
angular
  .module("FluidIntegrates")
  .component(
    "fieldBox",
    react2angular(
      fieldBox,
      [
        "title",
        "content",
      ],
    ),
  );
/**
 * @url: #/project/:project/events/:id/description
 * @page: eventcontent.html
 * @controllers: ["eventContentCtrl"]
 * @tag: <image-gallery/>
 */
angular
  .module("FluidIntegrates")
  .component(
    "imageGallery",
    react2angular(
      imageGallery,
      [
        "infinite",
        "items",
        "showBullets",
        "showFullscreenButton",
        "showIndex",
        "showNav",
        "showThumbnails",
        "thumbnailPosition",
      ],
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

/**
 * @url: #/project/:project/:id/comments
 * @page: findingcontent.html
 * @controllers: ["findingContentCtrl"]
 * @tag: <comment-box/>
 */
angular
  .module("FluidIntegrates")
  .component(
    "commentBox",
    react2angular(
      commentBox,
      [
        "type",
        "visible",
      ],
    ),
  );

/**
 * @url: #/project/:project/:id/exploit
 * @page: findingcontent.html
 * @controllers: ["findingContentCtrl"]
 * @tag: <exploit-view/>
 */
angular
  .module("FluidIntegrates")
  .component(
    "exploitView",
    react2angular(
      exploitView,
      [
        "code",
        "visible",
      ],
    ),
  );

/**
 * @url: #/project/:project/:id/tracking
 * @page: findingcontent.html
 * @controllers: ["findingContentCtrl"]
 * @tag: <tracking-view/>
 */
angular
  .module("FluidIntegrates")
  .component(
    "trackingView",
    react2angular(
      trackingView,
      [
        "openFindingsTitle",
        "openFindingsContent",
        "closedFindingsTitle",
        "closedFindingsContent",
        "closings",
        "discoveryDate",
        "discoveryText",
        "cycleText",
        "efectivenessText",
      ],
    ),
  );

/**
 * @url: /dashboard
 * @page: dashboard.html
 * @controllers: dashboardCtrl
 * @tag: <d-table/>
 */
angular
  .module("FluidIntegrates")
  .component(
   "dTable",
   react2angular(
     dataTable, [
       "dataset",
       "exportCsv",
       "headers",
       "onClickRow",
       "pageSize",
       "search",
       "title",
     ],
   ),
  );
