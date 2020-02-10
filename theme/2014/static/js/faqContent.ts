import { default as $ } from "jquery";

jQuery(() => {
    // Add acordion item class
    $(".sect3")
      .addClass("accordion-item");

    // Accordion section
    $("h4")
      .addClass("accordion-item-title db pv3 link black hover-red pointer black");

    // Section content
    $(".sect3 > div")
      .addClass("accordion-content b--black-20 pl3-l");

    $(".accordion-item-title")
      .on("click", (event: JQuery.ClickEvent) => {
          $(event.target)
          .nextAll(".accordion-content")
          .toggle("slow");
        });
});
