/* eslint-disable angular/file-name */
/**
 * @file index.ts
 * @description Controllers integrator for Integrates
 */
import angular from "angular";
import { react2angular } from "react2angular";
import { dataTable } from "./components/DataTable/index";
import frame from "./components/Frame/index";
import preloader from "./components/Preloader/index";
import button from "./components/RButton/index";
import fieldBox from "./scenes/Dashboard/components/FieldBox/index";
import { fileInput } from "./scenes/Dashboard/components/FileInput/index";
import imageGallery from "./scenes/Dashboard/components/ImageGallery/index";
import { Sidebar } from "./scenes/Dashboard/components/Sidebar";
import { eventDescriptionView } from "./scenes/Dashboard/containers/EventDescriptionView/index";
import Access from "./scenes/Login/components/Access/index";
import { welcomeView } from "./scenes/Registration/containers/WelcomeView";

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
       "enableRowSelection",
       "exportCsv",
       "headers",
       "id",
       "onClickRow",
       "pageSize",
       "search",
       "title",
     ],
   ),
  );

/**
 * @url: /dashboard
 * @page: dashboard.html
 * @controllers: dashboardCtrl
 * @tag: <r-button/>
 */
angular
  .module("FluidIntegrates")
  .component(
   "rButton",
   react2angular(
     button, [
       "bstyle",
       "btitle",
       "bicon",
       "onClickButton",
     ],
   ),
  );

  /**
   * @url: #/project/:project/events/:id/description
   * @page: eventcontent.html
   * @controllers: ["eventContentCtrl"]
   * @tag: <events-description-view/>
   */
angular
    .module("FluidIntegrates")
    .component(
      "eventDescriptionView",
      react2angular(
        eventDescriptionView, [
          "eventData",
          "eventId",
          "isActiveTab",
          "isEditable",
          "urlDescription",
          "urlEvidence",
        ],
      ),
    );

/**
 * @url: /dashboard
 * @page: users.html
 * @controllers: dashboardCtrl
 * @tag: <file-input/>
 */
angular
  .module("FluidIntegrates")
  .component(
   "fileInput",
   react2angular(
      fileInput, [
        "icon",
        "id",
        "type",
        "visible",
     ],
   ),
  );

/**
 * @url: /registration
 * @page: registration.html
 * @tag: <welcome-view/>
 */
angular
  .module("FluidIntegrates")
  .component(
    "welcomeView",
    react2angular(
      welcomeView, [
        "email",
        "username",
      ],
    ),
);

/**
 * @tag: <sidebar/>
 */
angular
  .module("FluidIntegrates")
  .component("sidebar", react2angular(Sidebar, ["onLogoutClick"]));
