import { default as $ } from "jquery";
/* This script creates a dropdown menu in rules index
 similar to Defends */

let rulescat: HTMLCollection; rulescat = document.getElementsByClassName("rulescat");
let i: number;
for (i = 0; i < rulescat.length; i += 1) {
  rulescat[i].addEventListener("click", (event: Event) => {
    (event.currentTarget as HTMLElement).classList.toggle("bg-fluid-lightgray");
    (event.currentTarget as HTMLElement).children[1].classList.toggle("rotate-90");
    const ruleslist: HTMLElement  = (event.currentTarget as HTMLElement).nextElementSibling as HTMLElement;
    ruleslist.classList.toggle("dn");
  });
}

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
