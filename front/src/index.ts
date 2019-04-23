/* eslint-disable angular/file-name */
/**
 * @file index.ts
 * @description Controllers integrator for Integrates
 */
import angular from "angular";
import { react2angular } from "react2angular";
import { dataTable } from "./components/DataTable/index";
import frame from "./components/Frame/index";
import button from "./components/RButton/index";
import { fileInput } from "./scenes/Dashboard/components/FileInput/index";
import { Sidebar } from "./scenes/Dashboard/components/Sidebar";
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
