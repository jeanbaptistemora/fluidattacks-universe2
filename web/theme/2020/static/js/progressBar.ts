export const progressBar: (() => void) = (): void => {
  const carouselWidth: HTMLElement = document.getElementById("carousel") as HTMLElement;
  const winScroll: number = carouselWidth.scrollLeft;
  const width: number = carouselWidth.scrollWidth - carouselWidth.clientWidth;
  // tslint:disable-next-line: no-magic-numbers
  const scrolled: number = (winScroll / width) * 100;
  let progress: HTMLElement;
  progress = document.getElementById("progress-bar") as HTMLElement;
  progress.style.width = `${scrolled}%`;
};

const carouselDiv: HTMLElement = document.getElementById("carousel") as HTMLElement;
carouselDiv.onscroll = (): void => { progressBar(); };
