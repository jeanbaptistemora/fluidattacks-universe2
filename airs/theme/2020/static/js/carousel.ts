const carousel: (() => void) = (): void => {
  const slider: HTMLElement = document.querySelector(".carousel") as HTMLElement;
  let isDown: boolean; isDown = false;
  let startX: number;
  let scrollLeft: number;

  slider.addEventListener("mousedown", (e: MouseEvent) => {
    isDown = true;
    slider.classList.add("active");
    startX = e.pageX - slider.offsetLeft;
    scrollLeft = slider.scrollLeft;
  });
  slider.addEventListener("mouseleave", () => {
    isDown = false;
    slider.classList.remove("active");
  });
  slider.addEventListener("mouseup", () => {
    isDown = false;
    slider.classList.remove("active");
  });
  slider.addEventListener("mousemove", (e: MouseEvent) => {
    if (!isDown) { return; }
    e.preventDefault();
    const x: number = e.pageX - slider.offsetLeft;
    // tslint:disable-next-line: no-magic-numbers
    const walk: number = (x - startX) * 3; // Scroll-fast
    slider.scrollLeft = scrollLeft - walk;
  });
};

carousel();
