/* eslint-disable angular/file-name */
/**
 * @file index.ts
 * @description Controllers integrator for Integrates
 */
import angular from "angular";
import { react2angular } from "react2angular";
import { fileInput } from "./scenes/Dashboard/components/FileInput/index";
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
