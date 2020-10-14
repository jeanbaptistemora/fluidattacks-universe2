import { default as $ } from "jquery";

import { logger, startBugsnag } from "./bugsnagErrorBoundary";
/*
Script to create a dropdown menu containing links to every
article of the main category clicked in the index of the KB.
If the category is clicked again, the menu disappears.
Used to improve the readability and presentation of the KB
articles.
*/

startBugsnag();

const defendscat: HTMLCollection = document.getElementsByClassName("defends-category");

const setDefends: (() => void) = (): void => {
  let i: number;
  for (i = 0; i < defendscat.length; i += 1) {
    defendscat[i].addEventListener("click", (event: Event) => {
      (event.currentTarget as HTMLElement).classList.toggle("active");
      const defendspanel: HTMLElement = (event.currentTarget as HTMLElement).nextElementSibling as HTMLElement;
      // tslint:disable-next-line: strict-boolean-expressions
      defendspanel.style.maxHeight ? defendspanel.style.maxHeight = "" :
      defendspanel.style.maxHeight = "max-content";
    });
  }
};

try {
  setDefends();
} catch (error) {
  logger.error("Error executing setDefends() function", error);
}

// Function to activate menu when redirected with an URL cotaining an anchor
const anchoredPanel: (() => void) = (): void => {
  $(() => {
      const anchor: string = window.location.hash;
      if (anchor !== "") {
        const span: (Node & ParentNode) | null = document.getElementById(anchor.replace("#", ""));
        const defendsCat: HTMLElement | (Node & ParentNode) | null = (span as Node).parentNode;
        const defendspanel: HTMLElement | null = (defendsCat as HTMLElement).nextElementSibling as HTMLElement;
        (defendsCat as HTMLElement).classList.toggle("active");
        // tslint:disable-next-line: strict-boolean-expressions
        defendspanel.style.maxHeight ? defendspanel.style.maxHeight = "" :
        defendspanel.style.maxHeight = "fit-content";
    }
  });
};

try {
  anchoredPanel();
} catch (error) {
  logger.error("Error executing contentHome() function", error);
}
