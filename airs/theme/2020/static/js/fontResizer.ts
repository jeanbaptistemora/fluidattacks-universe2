import { logger, startBugsnag } from "./bugsnagErrorBoundary";

startBugsnag();

const headers: HTMLCollectionOf<HTMLElement> =
  document.getElementsByClassName("responsive-text") as HTMLCollectionOf<HTMLElement>;
let count: number;

const flexFont: (() => void) = (): void => {

  for (count = 0; count < headers.length; count += 1) {
    const relFontSize: number = headers[count].offsetWidth * 0.15;
    headers[count].style.fontSize = `${relFontSize}px`;
  }
};

try {
  window.onload = (): void => {
    flexFont();
  };
} catch (error) {
  logger.error("Could not load the font size", error);
}

try {
  window.onresize = (): void => {
    flexFont();
  };
} catch (error) {
  logger.error("Could not resize the fontsize", error);
}
