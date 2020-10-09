import { default as $ } from "jquery";

// Generates an accordion list
const accordionItem: HTMLCollection = document.getElementsByClassName("sect2");
const accordionItemTitle: HTMLCollection = document.getElementsByTagName("h3");

const faqGen: (() => void) = (): void => {
  let counter: number;
  for (counter = 0; counter < accordionItem.length; counter += 1) {
    accordionItem[counter]
      .classList
      .add("accordion-item");
  }

  for (counter = 0; counter < accordionItemTitle.length; counter += 1) {
    accordionItemTitle[counter]
      .classList
      .add("accordion-item-title", "db", "pv3", "link", "black", "hover-red",
           "pointer", "black");

    accordionItemTitle[counter].addEventListener("click", (event: Event) => {
      $(event.currentTarget as HTMLElement)
        .nextAll(".accordion-content")
        .toggle("slow");
      $(event.currentTarget as HTMLElement)
        .children(".accordion-arrow")
        .toggleClass("rotate-180");
    });
  }
};

// Add arrows aside of each accordion title
const addArrow: (() => void) = (): void => {
  $(() => {
    $("h3")
      .append("<img src='../theme/images/faq/arrow-down.svg'\
      class='accordion-arrow w1 fr' alt='Arrow down icon'>"); // Insert content after matched selection
  });
};

const genFaq: (() => void) = (): void => {
  faqGen();
  addArrow();
};

genFaq();
