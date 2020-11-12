import { logger, startBugsnag } from "./bugsnagErrorBoundary";

startBugsnag();

const slideShow: (() => void) = (): void => {
  const slide1: HTMLElement = document.querySelector(".mySlide1") as HTMLElement;
  const dot1: HTMLElement = document.querySelector(".dot1") as HTMLElement;
  const slide2: HTMLElement = document.querySelector(".mySlide2") as HTMLElement;
  const dot2: HTMLElement = document.querySelector(".dot2") as HTMLElement;
  const slide3: HTMLElement = document.querySelector(".mySlide3") as HTMLElement;
  const dot3: HTMLElement = document.querySelector(".dot3") as HTMLElement;
  const homeSlides: HTMLElement = document.querySelector(".slideshow-home") as HTMLElement;

  dot1.addEventListener("click", (event: Event) => {
    (event.currentTarget as HTMLElement).classList.replace("bg-fluid-gray", "bg-fluid-red");
    dot2.classList.replace("bg-fluid-red", "bg-fluid-gray");
    dot3.classList.replace("bg-fluid-red", "bg-fluid-gray");
    slide1.classList.remove("dn");
    slide2.classList.add("dn");
    slide3.classList.add("dn");
    if (document.body.contains(homeSlides)) {
      if (homeSlides.classList.contains("bg-quote2")) {
        homeSlides.classList.replace("bg-quote2", "bg-quote1");
      } else if (homeSlides.classList.contains("bg-quote3")) {
        homeSlides.classList.replace("bg-quote3", "bg-quote1");
      }
    }
  });

  dot2.addEventListener("click", (event: Event) => {
    dot1.classList.replace("bg-fluid-red", "bg-fluid-gray");
    (event.currentTarget as HTMLElement).classList.replace("bg-fluid-gray", "bg-fluid-red");
    dot3.classList.replace("bg-fluid-red", "bg-fluid-gray");
    slide1.classList.add("dn");
    slide2.classList.remove("dn");
    slide3.classList.add("dn");
    if (document.body.contains(homeSlides)) {
      if (homeSlides.classList.contains("bg-quote1")) {
        homeSlides.classList.replace("bg-quote1", "bg-quote2");
      } else if (homeSlides.classList.contains("bg-quote3")) {
        homeSlides.classList.replace("bg-quote3", "bg-quote2");
      }
    }
  });

  dot3.addEventListener("click", (event: Event) => {
    dot1.classList.replace("bg-fluid-red", "bg-fluid-gray");
    dot2.classList.replace("bg-fluid-red", "bg-fluid-gray");
    (event.currentTarget as HTMLElement).classList.replace("bg-fluid-gray", "bg-fluid-red");
    slide1.classList.add("dn");
    slide2.classList.add("dn");
    slide3.classList.remove("dn");
    if (document.body.contains(homeSlides)) {
      if (homeSlides.classList.contains("bg-quote1")) {
        homeSlides.classList.replace("bg-quote1", "bg-quote3");
      } else if (homeSlides.classList.contains("bg-quote2")) {
        homeSlides.classList.replace("bg-quote2", "bg-quote3");
      }
    }
  });
};

try {
  slideShow();
} catch (error) {
  logger.error("Error executing slideShow() function", error);
}
