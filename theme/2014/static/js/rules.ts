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

// This section is for the expand/collapse all button

let categlist: HTMLElement; categlist = document.getElementsByClassName("categlist")[0];
categlist.addEventListener("click", (event: Event) => {
  (event.currentTarget as HTMLElement).classList.toggle("bg-fluid-lightgray");
  (event.currentTarget as HTMLElement).children[1].classList.toggle("rotate-90");
  let i: number;
  for (i = 0; i < rulescat.length; i += 1) {
      togglecat(rulescat[i]);
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
