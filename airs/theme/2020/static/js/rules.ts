import { default as $ } from "jquery";

import { logger, startBugsnag } from "./bugsnagErrorBoundary";

startBugsnag();

/* This script creates a dropdown menu in rules index
 similar to Defends */

// Function to toggle a category

const togglecat: ((categ: HTMLElement) => void) = (categ: HTMLElement):
  void => {
  categ.classList.toggle("ruleactive");
  categ.children[1].classList.toggle("rotate-180");
  const ruleslist: HTMLElement  = categ.nextElementSibling as HTMLElement;
  ruleslist.classList.toggle("dn");
};

let rulescat: HTMLCollection; rulescat = document.getElementsByClassName("rulescat");
let i: number;
for (i = 0; i < rulescat.length; i += 1) {
  rulescat[i].addEventListener("click", (event: Event) => {
    let categ: HTMLElement; categ = event.currentTarget as HTMLElement;

    try {
      togglecat(categ);
    } catch (error) {
      logger.error("Error executing togglecat() function", error);
    }
  });
}

// This section toggles visibility for the expand/collapse all buttons

const toggleswitch: ((switched: HTMLElement) => void) = (switched: HTMLElement):
  void => {
  switched.children[0].classList.toggle("dn");
  switched.children[1].classList.toggle("rotate-180");
  switched.children[1].classList.toggle("dn");
};

let expander: HTMLElement; expander = document.getElementsByClassName("expall")[0] as HTMLElement;
let collapser: HTMLElement; collapser = document.getElementsByClassName("collall")[0] as HTMLElement;

// This section expands all categories

expander.addEventListener("click", (event: Event) => {
  let collapsed: NodeListOf<HTMLElement>; collapsed = document.querySelectorAll(".rulescat:not(.ruleactive)");
  toggleswitch(expander);
  toggleswitch(collapser);

  let count: number;
  for (count = 0; count < collapsed.length; count += 1) {
    try {
      togglecat(collapsed[count]);
    } catch (error) {
      logger.error("Error executing togglecat() function", error);
    }
  }
});

// This section collapses all categories

collapser.addEventListener("click", (event: Event) => {
  let expanded: NodeListOf<HTMLElement>; expanded = document.querySelectorAll(".ruleactive");
  toggleswitch(expander);
  toggleswitch(collapser);

  let count: number;
  for (count = 0; count < expanded.length; count += 1) {
    try {
      togglecat(expanded[count]);
    } catch (error) {
      logger.error("Error executing togglecat() function", error);
    }
  }
});

// Activate the list when the category is referenced through the url

const activatePanel: (() => void) = (): void => {
  $(() => {
    let anchor: string; anchor = window.location.hash;
    if (anchor !== "") {
      let span: HTMLElement;
      span = document.getElementById(anchor.replace("#", "")) as HTMLElement;
      let category: HTMLElement;
      category = span.parentNode as HTMLElement;
      const img: HTMLElement = category.nextElementSibling as HTMLElement;
      img.classList.toggle("rotate-90");
      let div: HTMLElement = category.parentNode as HTMLElement;
      div = div.nextElementSibling as HTMLElement;
      div.classList.toggle("dn");
    }
  });
};

try {
  activatePanel();
} catch (error) {
  logger.error("Error executing activatePanel() function", error);
}
