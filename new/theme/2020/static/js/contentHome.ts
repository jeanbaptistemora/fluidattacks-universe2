import { default as $ } from "jquery";

import { animationById } from "./jqueryFunctions";

const contentHome: (() => void) = (): void => {
  $(() => {
    $('input:radio[name="menu1"]')
      .on("change", () => {

        animationById("#op1", "checked", ".fixes", ".drills, .forces",
                      "dn fadein", "dn", "fadein");
        animationById("#op2", "checked", ".drills", ".fixes, .forces",
                      "dn fadein active", "dn", "fadein");
        animationById("#op3", "checked", ".forces", ".fixes, .drills",
                      "dn fadein active", "dn", "fadein");
    });
    $('input:radio[name="menu2"]')
      .on("change", () => {

        animationById("#op5", "checked", ".continuous", ".oneshot",
                      "dn fadein", "dn", "fadein");
        animationById("#op6", "checked", ".oneshot", ".continuous",
                      "dn fadein active", "dn", "fadein");
    });
    $('input:radio[name="menu3"]')
    .on("change", () => {

      animationById("#products-title", "checked", ".products-list", ".usecases-list, .aboutus-list",
                    "dn fadein active", "dn", "fadein");
      animationById("#usecases-title", "checked", ".usecases-list", ".products-list, .aboutus-list",
                    "dn fadein active", "dn", "fadein");
      animationById("#aboutus-title", "checked", ".aboutus-list", ".products-list, .usecases-list",
                    "dn fadein active", "dn", "fadein");
    });
  });
};

contentHome();
