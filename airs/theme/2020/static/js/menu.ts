import { logger, startBugsnag } from "./bugsnagErrorBoundary";

startBugsnag();

const mySidenavXl: HTMLElement = document.getElementById("mySidenavXl") as HTMLElement;
const openbtn: HTMLElement = document.getElementById("openbtn") as HTMLElement;
const closebtn: HTMLElement = document.getElementById("closebtn") as HTMLElement;
const closebtnS: HTMLElement = document.getElementById("closebtnS") as HTMLElement;
const mySidenavS: HTMLElement = document.getElementById("mySidenavS") as HTMLElement;

const toggleNavXl: (() => void) = (): void => {
  mySidenavXl.classList.toggle("dn");
};

const slideNavS: (() => void) = (): void => {
  mySidenavS.style.width = "100%";
};

const closeNavS: (() => void) = (): void => {
  mySidenavS.style.width = "0";
};

const menu: (() => void) = (): void => {
  openbtn.addEventListener("click", () => {
    toggleNavXl();
    slideNavS();
  });

  closebtn.addEventListener("click", () => {
    toggleNavXl();
  });

  closebtnS.addEventListener("click", () => {
    closeNavS();
  });
};

try {
  menu();
} catch (error) {
  logger.error("Error executing menu() function", error);
}
