import _ from "lodash";
import { FormErrors } from "redux-form";

export const focusError: ((errors: FormErrors<FormData>) => void) = (): void => {
  const invalidField: HTMLElement | null = document.getElementById("validationError");
  if (!_.isNil(invalidField)) {
    invalidField.scrollIntoView({ behavior: "smooth" });
  }
};
