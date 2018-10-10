import _ from "lodash";
import { isRequired } from "revalidate";

export const required: typeof isRequired = isRequired({
  message: "This field is required.",
});

export const validEmail: ((arg1: string) => string | undefined) =
  (value: string): string | undefined => {
  const pattern: RegExp = /^[a-zA-Z0-9.!#$%&’*+\/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/i;
  if (_.isEmpty(value) || !pattern.test(value)) {
    return "The email format is not valid.";
  } else {
    return undefined;
  }
};
