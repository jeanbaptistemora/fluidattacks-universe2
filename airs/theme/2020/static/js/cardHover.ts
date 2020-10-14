import { logger, startBugsnag } from "./bugsnagErrorBoundary";

startBugsnag();

const accordions: HTMLCollection = document.getElementsByClassName("accordion");
const readmores: HTMLCollection = document.getElementsByClassName("readmore");

let count: number;

const setAccordions: (() => void) = (): void => {
  for (count = 0; count < accordions.length; count += 1) {
    accordions[count].addEventListener("click", (event: Event) => {
      (event.currentTarget as HTMLElement).classList.toggle("active");
      const panel: HTMLElement = (event.currentTarget as HTMLElement).nextElementSibling as HTMLElement;
      const arrow: HTMLElement = (panel.nextElementSibling as HTMLElement).children[1] as HTMLElement;

      arrow.classList.toggle("rotate-180");
      (event.currentTarget as HTMLElement).children[2].classList.toggle("dn");
      (panel.nextElementSibling as HTMLElement).classList.toggle("dn");

      // tslint:disable-next-line: strict-boolean-expressions
      panel.style.height ?
      panel.style.height = ""
      : panel.style.height = "22.5rem";

    });
  }
};

try {
  setAccordions();
} catch (error) {
  logger.error("Error executing setAccordions() function", error);
}

const setReadmores: (() => void) = (): void => {
  for (count = 0; count < readmores.length; count += 1) {
    readmores[count].addEventListener("click", (event: Event) => {

      const current: HTMLElement = event.currentTarget as HTMLElement;
      current.classList.toggle("active");
      const panel: HTMLElement = current.previousElementSibling as HTMLElement;
      const mainbt: HTMLElement = panel.previousElementSibling as HTMLElement;

      if (mainbt.classList.contains("active")) {
        mainbt.click();
      }
    });
  }
};

try {
  setReadmores();
} catch (error) {
  logger.error("Error executing setReadmores() function", error);
}
