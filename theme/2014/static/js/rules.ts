import { default as $ } from "jquery";
/* This script creates a dropdown menu in rules index
 similar to Defends */

// Function to toggle a category

let togglecat: function; togglecat = function(categ: HTMLElement){
  categ.classList.toggle("bg-fluid-lightgray");
  categ.children[1].classList.toggle("rotate-90");
  const ruleslist: HTMLElement  = categ.nextElementSibling as HTMLElement;
  ruleslist.classList.toggle("dn");
};

let rulescat: HTMLCollection; rulescat = document.getElementsByClassName("rulescat");
let i: number;
for (i = 0; i < rulescat.length; i += 1) {
  rulescat[i].addEventListener("click", (event: Event) => {
    let categ: HTMLElement; categ = event.currentTarget as HTMLElement;
    togglecat(categ);
  });
}

// This section toggles visibility for the expand/collapse all buttons

let toggleswitch: function; toggleswitch = function(switched: HTMLElement){
  switched.children[0].classList.toggle("dn");
  switched.children[1].classList.toggle("rotate-90");
  switched.children[1].classList.toggle("dn");
}

let expander: HTMLElement; expander = document.getElementsByClassName("expall")[0];
let collapser: HTMLElement; collapser = document.getElementsByClassName("collall")[0];

// This section expands all categories

expander.addEventListener("click", (event: Event) => {
  let collapsed: HTMLCollection; collapsed = document.querySelectorAll(".rulescat:not(.bg-fluid-lightgray)");
  toggleswitch(expander);
  toggleswitch(collapser);

  let i: number;
  for (i = 0; i < collapsed.length; i += 1) {
      togglecat(collapsed[i]);
  }
});

// This section collapses all categories

collapser.addEventListener("click", (event: Event) => {
  let expanded: HTMLCollection; expanded = document.querySelectorAll(".rulescat.bg-fluid-lightgray");
  toggleswitch(expander);
  toggleswitch(collapser);

  let i: number;
  for (i = 0; i < expanded.length; i += 1) {
      togglecat(expanded[i]);
  }
});

// Activate the list when the category is referenced through the url

$(() => {
    let anchor: string; anchor = window.location.hash;
    if (anchor !== "") {
      let span: HTMLElement;
      span = document.getElementById(anchor.replace("#", "")) as HTMLElement;
      let category: HTMLElement;
      category = span.parentNode as HTMLElement;
      category.classList.toggle("bg-fluid-lightgray");
      category.children[1].classList.toggle("rotate-90");
      const list: HTMLElement = category.nextElementSibling as HTMLElement;
      list.classList.toggle("dn");
    }
});
