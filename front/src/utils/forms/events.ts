import _ from "lodash";

export const focusError: () => void = (): void => {
  const invalidField: HTMLElement | null = document.getElementById(
    "validationError"
  );
  if (!_.isNil(invalidField)) {
    invalidField.scrollIntoView({ behavior: "smooth" });
  }
};
