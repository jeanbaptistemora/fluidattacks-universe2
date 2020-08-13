import { default as $ } from "jquery";

export const toggleClasses: ((elementClass: string, toggleStyles: string)
  => void) = (elementClass: string, toggleStyles: string): void => {
  $(elementClass)
    .toggleClass(toggleStyles);
};

export const addClasses: ((classNames: string, addedStyles: string)
  => void) = (classNames: string, addedStyles: string): void => {
    $(classNames)
      .addClass(addedStyles);
};

export const removeClasses: ((classNames: string, removedClasses: string)
  => void) = (classNames: string, removedClasses: string): void => {
    $(classNames)
      .removeClass(removedClasses);
};

export const animationById: (
  (inputId: string, prop: string, elementClass: string, referenceClasses: string, toggleStyles: string,
   addedClasses: string, removedClasses: string) => void) = (
    inputId: string, prop: string, elementClass: string, referenceClasses: string, toggleStyles: string,
    addedClasses: string, removedClasses: string): void => {
  if ($(inputId)
    .prop(prop)) {
    toggleClasses(elementClass, toggleStyles);
    addClasses(referenceClasses, addedClasses);
    removeClasses(referenceClasses, removedClasses);
  }
};

export const parallaxEffect: ((element: string) => void) =
  (element: string): void => {
    const parallaxElement: JQuery = $(element);
    const parallaxQuantity: number = parallaxElement.length;
    window.requestAnimationFrame(() => {
      let count: number;
      for (count = 0; count < parallaxQuantity; count += 1) {
        const currentElement: JQuery = parallaxElement.eq(count);
        const windowTop: number = $(window)
                          .scrollTop() as number;
        const elementTop: number = (currentElement.offset() as JQueryCoordinates).top;
        const elementHeight: number = currentElement.height() as number;
        const viewPortHeight: number = window.innerHeight * 0.4 - elementHeight * 0.4;
        const scrolled: number = windowTop - elementTop + viewPortHeight;
        currentElement.css({
          transform: `translate3d(0, ${scrolled * -0.2}px, 0)`,
        });
      }
    });
};
