
let slideIndex: number; slideIndex = 1;
let myTimer: NodeJS.Timeout;

const contactSlider: (() => void) = (): void => {
  window.addEventListener("load", () => {
      // tslint:disable-next-line: no-use-before-declare
      showSlides(slideIndex);
      // tslint:disable-next-line: no-use-before-declare
      myTimer = setInterval(() => { plusSlides(1); }, 4000);
  });

  // NEXT AND PREVIOUS CONTROL
  const plusSlides: ((n: number) => void) = (n: number): void => {
    clearInterval(myTimer);
    if (n < 0) {
        // tslint:disable-next-line: no-use-before-declare
        showSlides(slideIndex -= 1);
    } else {
    // tslint:disable-next-line: no-use-before-declare
    showSlides(slideIndex += 1);
    }

    // COMMENT OUT THE LINES BELOW TO KEEP ARROWS PART OF MOUSEENTER PAUSE/RESUME

    // tslint:disable-next-line: prefer-conditional-expression
    if (n === -1) {
        myTimer = setInterval(() => {plusSlides(n + 2); }, 4000);
    } else {
        myTimer = setInterval(() => {plusSlides(n + 1); }, 4000);
    }
  };

  const showSlides: ((n: number) => void) = (n: number): void => {
  let i: number;
  // tslint:disable-next-line: typedef
  const slides = document.getElementsByClassName("mySlides") as HTMLCollectionOf<HTMLElement>;
  // tslint:disable-next-line: typedef
  const dots = document.getElementsByClassName("dot") as HTMLCollectionOf<HTMLElement>;
  if (n > slides.length) {slideIndex = 1; }
  if (n < 1) {slideIndex = slides.length; }
  for (i = 0; i < slides.length; i += 1) {
      slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i += 1) {
      dots[i].className = dots[i].className.replace(" active-slide", "");
  }
  slides[slideIndex - 1].style.display = "block";
  dots[slideIndex - 1].className += " active-slide";
  };

  // Controls the current slide and resets interval if needed
  const currentSlide: ((n: number) => void) = (n: number): void => {
      clearInterval(myTimer);
      myTimer = setInterval(() => {plusSlides(n + 1); }, 4000);
      showSlides(slideIndex = n);
  };

};

contactSlider();
