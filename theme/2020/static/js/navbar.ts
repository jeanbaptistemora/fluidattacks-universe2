
const navbar: (() => void) = (): void => {
  let prevScrollpos: number = window.pageYOffset;

  window.onscroll = (): void => {
  const currentScrollPos: number = window.pageYOffset;
  const navbarElement: HTMLElement = document.getElementById("navbar") as HTMLElement;
  prevScrollpos > currentScrollPos ?
  navbarElement.style.top = "0" :
  navbarElement.style.top = "-110px";

  prevScrollpos = currentScrollPos;
  };
};

navbar();
