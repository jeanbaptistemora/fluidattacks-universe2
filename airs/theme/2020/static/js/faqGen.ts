import { default as $ } from "jquery";

import { logger, startBugsnag } from "./bugsnagErrorBoundary";

startBugsnag();

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
      class='accordion-arrow w1 v-mid mr0 ml-auto' alt='Arrow down icon'>");
  });
};

const genFaq: (() => void) = (): void => {
  faqGen();
  addArrow();
};

try {
  genFaq();
} catch (error) {
  logger.error("Error executing genFaq() function", error);
}

const loadMore: (() => void) = (): void => {
  $(() => {
    $(".accordion-item")
      .slice(0, 10)
      .show();

    $("#showMore")
    // tslint:disable-next-line:deprecation
      .on("click", (event: Event) => {
      event.preventDefault();
      $(".accordion-item:hidden")
        .slice(0, 10)
        .slideDown();
      if ($(".accordion-item:hidden").length === 0) {
        $("#showLess")
          .fadeIn("slow");
        $("#showMore")
          .hide();
      }
      $("html,body")
        .animate({
          scrollTop: ($(event.currentTarget as HTMLElement)
                      .offset() as JQuery.PlainObject).bottom,
        },       500);

    });
    $("#showLess")
    // tslint:disable-next-line:deprecation
      .on("click", (event: Event) => {
      event.preventDefault();
      $(".accordion-item:not(:lt(10))")
        .fadeOut();
      $("#showMore")
        .fadeIn("slow");
      $("#showLess")
        .hide();

      $("html,body")
        .animate({
          scrollTop: ($(event.currentTarget as HTMLElement)
                      .offset() as JQuery.PlainObject).top,
        },       500);
    });

  });
};

try {
  loadMore();
} catch (error) {
  logger.error("Error executing loadMore() function", error);
}
