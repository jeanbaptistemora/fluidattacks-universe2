import { default as $ } from "jquery";

import { animationById } from "./jqueryFunctions";

const contentHome: (() => void) = (): void => {
  $(() => {
    $('input:radio[name="menu1"]')
      .on("change", () => {

        animationById("#op1", "checked", ".fixes", ".skims, .drills, .forces",
                      "dn fadein", "dn", "fadein");
        animationById("#op2", "checked", ".skims", ".fixes, .drills, .forces",
                      "dn fadein active", "dn", "fadein");
        animationById("#op3", "checked", ".drills", ".fixes, .skims, .forces",
                      "dn fadein active", "dn", "fadein");
        animationById("#op4", "checked", ".forces", ".fixes, .skims, .drills",
                      "dn fadein active", "dn", "fadein");
    });
    $('input:radio[name="menu2"]')
      .on("change", () => {

        animationById("#op5", "checked", ".continuous", ".oneshot",
                      "dn fadein", "dn", "fadein");
        animationById("#op6", "checked", ".oneshot", ".continuous",
                      "dn fadein active", "dn", "fadein");
    });
  });
};

contentHome();
