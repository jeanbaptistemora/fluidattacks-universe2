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
import indicatorBox from "./scenes/Dashboard/components/IndicatorBox/index";
import indicatorGraph from "./scenes/Dashboard/components/IndicatorGraph/index";
import { eventDescriptionHeader, eventDescriptionView } from "./scenes/Dashboard/containers/EventDescriptionView/index";
import { eventsView } from "./scenes/Dashboard/containers/EventsView/index";
import { indicatorsView } from "./scenes/Dashboard/containers/IndicatorsView/index";
import { projectCommentsView } from "./scenes/Dashboard/containers/ProjectCommentsView";
import { projectUsersView } from "./scenes/Dashboard/containers/ProjectUsersView/index";
import { resourcesView } from "./scenes/Dashboard/containers/ResourcesView/index";
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
 * @url: #/project/:name/indicators
 * @page: indicators.html
 * @controllers: ["projectIndicatorsCtrl"]
 * @tag: <indicators-view/>
 */
angular
  .module("FluidIntegrates")
  .component(
    "indicatorsView",
    react2angular(
      indicatorsView,
      [
        "projectName",
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

angular
  .module("FluidIntegrates")
  .component(
    "resourcesView",
    react2angular(
      resourcesView, [
        "projectName",
      ],
    ),
  );

/**
 * @url: #/project/:project/events/
 * @page: events.html
 * @controllers: ["projectEventsCtrl"]
 * @tag: <events-view/>
 */
angular
  .module("FluidIntegrates")
  .component(
    "eventsView",
    react2angular(
      eventsView, [
        "projectName",
        "onClickRow",
        "onResume",
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
          "eventEdit",
          "eventUpdate",
          "isEditable",
          "hasAccessibility",
          "hasAffectedComponents",
        ],
      ),
    );

    /**
     * @url: #/project/:project/events/:id/description
     * @page: eventcontent.html
     * @controllers: ["eventContentCtrl"]
     * @tag: <events-description-header/>
     */
angular
      .module("FluidIntegrates")
      .component(
        "eventDescriptionHeader",
        react2angular(
          eventDescriptionHeader, [
            "eventData",
            "urlDescription",
            "urlEvidence",
            "isActiveTab",
            "hasEvidence",
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
 * @url: #/project/:project/users
 * @page: users.html
 * @controllers: projectUsersCtrl
 * @tag: <project-Users-view/>
 */
angular
  .module("FluidIntegrates")
  .component(
   "projectUsersView",
   react2angular(
      projectUsersView, [
        "projectName",
        "userRole",
     ],
   ),
  );

/**
 * @url: #/project/:project/comments
 * @page: comments.html
 * @controllers: projectCommentsCtrl
 * @tag: <project-comments-view/>
 */
angular
  .module("FluidIntegrates")
  .component(
    "projectCommentsView",
    react2angular(
      projectCommentsView, [
        "projectName",
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
