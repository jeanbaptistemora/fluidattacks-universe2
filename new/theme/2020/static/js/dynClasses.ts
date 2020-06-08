import { default as $ } from "jquery";

import { addClasses } from "./jqueryFunctions";

const dynClasses: (() => void) = (): void => {
  $(() => {
    addClasses(".use-cases > .sect1 > h2", "f2-l tc-ns tl f3 w6-ns center w-90");

    addClasses(".use-cases > .sect1 > .sectionbody",
               "tl fw1 w40-l w-50-m w90-s center f4-ns f5 lh-2");

    addClasses(".products > .sect1 > h2", "f1-ns f3 tc w6-ns center w-90");

    addClasses(".products > .sect1 > .sectionbody",
               "fw1 w-40-l w-50-m w90-s center f3-ns f5 lh-2");

    addClasses(".forces-feature > h2 > a", "c-lightblack no-underline");

    addClasses(".forces-feature > .paragraph > p > a", "c-lightblack no-underline");

    addClasses(".intl-tel-input", "db");

  });
};

dynClasses();
