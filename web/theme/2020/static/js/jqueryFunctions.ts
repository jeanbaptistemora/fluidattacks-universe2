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
