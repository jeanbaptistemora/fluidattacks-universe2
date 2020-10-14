import { logger, startBugsnag } from "./bugsnagErrorBoundary";

startBugsnag();

const navbar: (() => void) = (): void => {
  let prevScrollpos: number = window.pageYOffset;

  window.onscroll = (): void => {
  const currentScrollPos: number = window.pageYOffset;
  const navbarElement: HTMLElement = document.getElementById("navbar") as HTMLElement;

  prevScrollpos > currentScrollPos ?
  navbarElement.style.top = "0" :
  navbarElement.style.top = "-104px";

  prevScrollpos = currentScrollPos;
  };
};

try {
  navbar();
} catch (error) {
  logger.error("Error executing navbar() function", error);
}
