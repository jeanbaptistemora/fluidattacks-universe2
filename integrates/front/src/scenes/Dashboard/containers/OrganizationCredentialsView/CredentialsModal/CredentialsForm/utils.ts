import type { BaseSchema, InferType } from "yup";
import { lazy, object, string } from "yup";
import type { TypedSchema } from "yup/lib/util/types";

import type { IFormValues } from "./types";

import { translate } from "utils/translations/translate";

const validateSchema = (): InferType<TypedSchema> =>
  lazy(
    (values: IFormValues): BaseSchema =>
      object({
        auth: string(),
        key: string()
          .when("type", {
            is: "SSH",
            otherwise: string(),
            then: string().required(translate.t("validations.required")),
          })
          .test(
            "hasSshFormat",
            translate.t("validations.invalidSshFormat"),
            (value): boolean => {
              const regex =
                /^-{5}BEGIN OPENSSH PRIVATE KEY-{5}\n(?:[a-zA-Z0-9+/=]+\n)+-{5}END OPENSSH PRIVATE KEY-{5}\n?$/u;

              if (value === undefined || values.type !== "SSH") {
                return true;
              }

              return regex.test(value);
            }
          ),
        name: string().when("type", {
          is: undefined,
          otherwise: string().required(translate.t("validations.required")),
          then: string(),
        }),
        password: string().when("type", {
          is: values.auth === "USER" ? "HTTPS" : "",
          otherwise: string(),
          then: string().required(translate.t("validations.required")),
        }),
        token: string().when("type", {
          is: values.auth === "TOKEN" ? "HTTPS" : "",
          otherwise: string(),
          then: string().required(translate.t("validations.required")),
        }),
        type: string().required(translate.t("validations.required")),
        user: string().when("type", {
          is: values.auth === "USER" ? "HTTPS" : "",
          otherwise: string(),
          then: string().required(translate.t("validations.required")),
        }),
      })
  );

export { validateSchema };
