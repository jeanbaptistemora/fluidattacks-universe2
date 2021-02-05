import { default as $ } from "jquery";
import { add } from "lodash";

import { logger, startBugsnag } from "./bugsnagErrorBoundary";
import { addClasses } from "./jqueryFunctions";

startBugsnag();

const dynClasses: (() => void) = (): void => {
  $(() => {
    addClasses(".services > .sect1 > h2", "f2-l tc-ns tl f3 w6-ns center w-90");

    addClasses(".services > .sect1 > .sectionbody",
               "tl fw1 w40-l w-50-m w90-s center f4-ns f5 lh-2");

    addClasses(".products > .sect1 > h2", "f1-ns f3 tc w6-ns center w-90");

    addClasses(".products > .sect1 > .sectionbody",
               "fw1 w-40-l w-50-m w90-s center f3-ns f5 lh-2");

    addClasses(".forces-feature > h2 > a", "c-lightblack no-underline");

    addClasses(".forces-feature > .paragraph > p > a", "c-lightblack no-underline");

    addClasses(".intl-tel-input", "db");

    addClasses(".solution-benefits > .sect2", "dib-l");

    addClasses(".other-features > .sect2", "w-benefit dib-l");

    addClasses(".product-features > .sect2", "w-benefit dib-l");

    addClasses(".faq-list > .sect2 > div", "accordion-content b--black-20 pl3-l");

    addClasses(".compliance-page > .sect1 > h2", "f1-ns f2");

    addClasses(".plans-feat > .flex > .sect2", "b--light-gray b--solid br3 bw1 mb3 mh3 pb5 ph4 tc");
    addClasses(".plans-feat > .flex > .sect2 > .paragraph", "tl");

    if ($("div")
        .hasClass("contact-page")) {
      $(".footer-component")
        .addClass("dn-s");
    }

    addClasses(".feature-content a", "fw8 c-fluid-bk hv-fluid-rd no-underline");
    addClasses(".button-asserts", "br2 bannerbt hv-bt-fluid-rd ph4-l ph5 pv2 bt-trans white b roboto pointer");

    $(".button-asserts")
      .parent()
      .parent()
      .addClass("tc");
  });
};

try {
  dynClasses();
} catch (error) {
  logger.error("Error executing dynClasses() function", error);
}
