import { default as $ } from "jquery";

import { logger, startBugsnag } from "./bugsnagErrorBoundary";

startBugsnag();

const clientsFilter: (() => void) = (): void => {
  $('input:radio[name="menu-clients"]')
  .on("change", () => {
    if ($("#gall")
      .prop("checked")) {
        $(".banking, .healthcare, .human-resources, .automotive, .technology, " +
          ".pharmaceuticals, .oil-energy, .telecommunications, .airlines")
          .removeClass("dn")
          .addClass("dt-ns");
      }
    if ($("#g1")
      .prop("checked")) {
        $(".healthcare, .human-resources, .automotive, .technology, " +
          ".pharmaceuticals, .oil-energy, .telecommunications, .airlines")
          .removeClass("dt-ns")
          .addClass("dn");
        $(".banking")
          .removeClass("dn")
          .addClass("dt-ns");
      }
    if ($("#g2")
      .prop("checked")) {
        $(".healthcare, .human-resources, .automotive, .technology, " +
        ".pharmaceuticals, .telecommunications, .airlines, .banking")
          .removeClass("dt-ns")
          .addClass("dn");
        $(".oil-energy")
          .removeClass("dn")
          .addClass("dt-ns");
      }
    if ($("#g3")
      .prop("checked")) {
        $(".banking, .healthcare, .human-resources, .technology, " +
        ".pharmaceuticals, .oil-energy, .telecommunications, .airlines")
          .removeClass("dt-ns")
          .addClass("dn");
        $(".automotive")
          .removeClass("dn")
          .addClass("dt-ns");
      }
    if ($("#g4")
      .prop("checked")) {
        $(".banking, .healthcare, .human-resources, .automotive, .technology, " +
          ".oil-energy, .telecommunications, .airlines")
          .removeClass("dt-ns")
          .addClass("dn");
        $(".pharmaceuticals")
          .removeClass("dn")
          .addClass("dt-ns");
      }
    if ($("#g5")
      .prop("checked")) {
        $(".banking, .human-resources, .automotive, .technology, " +
          ".pharmaceuticals, .oil-energy, .telecommunications, .airlines")
          .removeClass("dt-ns")
          .addClass("dn");
        $(".healthcare")
          .removeClass("dn")
          .addClass("dt-ns");
      }
    if ($("#g6")
      .prop("checked")) {
        $(".banking, .healthcare, .human-resources, .automotive, .technology, " +
          ".pharmaceuticals, .oil-energy, .telecommunications")
          .removeClass("dt-ns")
          .addClass("dn");
        $(".airlines")
          .removeClass("dn")
          .addClass("dt-ns");
      }
    if ($("#g7")
      .prop("checked")) {
        $(".banking, .healthcare, .human-resources, .automotive, .technology, " +
          ".pharmaceuticals, .oil-energy, .airlines")
          .removeClass("dt-ns")
          .addClass("dn");
        $(".telecommunications")
          .removeClass("dn")
          .addClass("dt-ns");
      }
    if ($("#g8")
      .prop("checked")) {
        $(".banking, .healthcare, .automotive, .technology, " +
          ".pharmaceuticals, .oil-energy, .telecommunications, .airlines")
          .removeClass("dt-ns")
          .addClass("dn");
        $(".human-resources")
          .removeClass("dn")
          .addClass("dt-ns");
      }
    if ($("#g9")
      .prop("checked")) {
        $(".banking, .healthcare, .human-resources, .automotive, " +
          "S.pharmaceuticals, .oil-energy, .telecommunications, .airlines")
          .removeClass("dt-ns")
          .addClass("dn");
        $(".technology")
          .removeClass("dn")
          .addClass("dt-ns");
      }
  });
};

try {
  clientsFilter();
} catch (error) {
  logger.error("Error executing clientsFilter() function", error);
}

const scrollDiv: HTMLElement = document.getElementById("scrollDiv") as HTMLElement;
const rightArrow: HTMLElement = document.getElementById("right-arrow") as HTMLElement;
const leftArrow: HTMLElement = document.getElementById("left-arrow") as HTMLElement;

const menuScroll: ((menuOffset: number) => void) =
  (menuOffset: number): void => {
  scrollDiv.style.marginLeft = `${-menuOffset}+px`;
};

const scrollRight: (() => void) = (): void => {
  rightArrow.addEventListener("click", () => {
    menuScroll(100);
  });
};

try {
  scrollRight();
} catch (error) {
  logger.error("Error executing scrollRight() function", error);
}

const scrollLeft: (() => void) = (): void => {
  leftArrow.addEventListener("click", () => {
    menuScroll(0);
  });
};

try {
  scrollLeft();
} catch (error) {
  logger.error("Error executing scrollLeft() function", error);
}
