import gsap from "gsap";

const fadeIn: (() => void) = (): void => {
  gsap.from(".turbine-text", {
    duration: 3,
    ease: "power4.in",
    opacity: 0,
  });
};

const transition: (() => void) = (): void => {
  gsap.from("#turbine", {
    duration: 2.5,
    ease: "expo.out",
    scale: 0.25,
    x: -9999,
  });
};

const animate: (() => void) = (): void => {
  gsap.to("#turbine", {
    onComplete: transition,
  });
  gsap.to(".turbine-text", {
    onComplete: fadeIn,
  });
};

animate();
