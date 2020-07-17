import { default as $ } from "jquery";

import { animationById, toggleClasses } from "./jqueryFunctions";

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
    $('input:radio[name="menu4"]')
    .on("change", () => {
      if ($("#op7")
        .prop("checked")) {
          $(".report, .webinar, .datasheet, .ebook")
            .removeClass("dn")
            .addClass("dt-ns");
        }
      if ($("#op8")
        .prop("checked")) {
          $(".report, .webinar, .datasheet")
            .removeClass("dt-ns")
            .addClass("dn");
          $(".ebook")
            .removeClass("dn")
            .addClass("dt-ns");
        }
      if ($("#op9")
        .prop("checked")) {
          $(".webinar, .datasheet, .ebook")
            .removeClass("dt-ns")
            .addClass("dn");
          $(".report")
            .removeClass("dn")
            .addClass("dt-ns");
        }
      if ($("#op10")
        .prop("checked")) {
          $(".report, .datasheet, .ebook")
            .removeClass("dt-ns")
            .addClass("dn");
          $(".webinar")
            .removeClass("dn")
            .addClass("dt-ns");
        }
      if ($("#op11")
        .prop("checked")) {
          $(".report, .webinar, .ebook")
            .removeClass("dt-ns")
            .addClass("dn");
          $(".datasheet")
            .removeClass("dn")
            .addClass("dt-ns");
        }
    });
    $(".search-icon")
      .on("click", () => {
        $(".search-input")
          .animate({height: "toggle"});
        $(".search-div")
          .animate({height: "toggle"});
      });
  });
};

contentHome();
