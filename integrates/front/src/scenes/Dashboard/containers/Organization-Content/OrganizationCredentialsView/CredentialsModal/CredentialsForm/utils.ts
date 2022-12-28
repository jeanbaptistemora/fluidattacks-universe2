import type { BaseSchema, InferType } from "yup";
import { lazy, object, string } from "yup";
import type { TypedSchema } from "yup/lib/util/types";

import type { IFormValues } from "./types";

import { translate } from "utils/translations/translate";
import { regExps } from "utils/validations";

const MAX_FIELD_LENGTH = 100;
const MIN_FIELD_LENGTH = 40;

const validateSchema = (): InferType<TypedSchema> =>
  lazy(
    (values: IFormValues): BaseSchema =>
      object({
        auth: string(),
        azureOrganization: string().when(["newSecrets", "type", "isPat"], {
          is: (newSecrets: boolean, type: string, isPat: boolean): boolean =>
            newSecrets &&
            type === (values.auth === "TOKEN" ? "HTTPS" : "") &&
            isPat,
          otherwise: string(),
          then: string()
            .required(translate.t("validations.required"))
            .test(
              "hasValidValue",
              translate.t("validations.invalidSpaceField"),
              (value): boolean => {
                const regex = /\S/u;
                if (value === undefined) {
                  return true;
                }

                return regex.test(value);
              }
            ),
        }),
        key: string()
          .when(["newSecrets", "type"], {
            is: (newSecrets: boolean, type: string): boolean =>
              newSecrets && type === "SSH",
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
        name: string()
          .when("type", {
            is: undefined,
            otherwise: string().required(translate.t("validations.required")),
            then: string(),
          })
          .test(
            "hasValidValue",
            translate.t("validations.invalidSpaceField"),
            (value): boolean => {
              const regex = /\S/u;
              if (value === undefined) {
                return true;
              }

              return regex.test(value);
            }
          ),
        password: string()
          .when(["newSecrets", "type"], {
            is: (newSecrets: boolean, type: string): boolean =>
              newSecrets && type === (values.auth === "USER" ? "HTTPS" : ""),
            otherwise: string(),
            then: string()
              .required(translate.t("validations.required"))
              .test(
                "startWithLetter",
                translate.t("validations.credentialsModal.startWithLetter"),
                (value: string | undefined): boolean => {
                  if (value === undefined || value === "") {
                    return false;
                  }

                  return regExps.alphabetic.test(value[0]);
                }
              )
              .test(
                "includeNumber",
                translate.t("validations.credentialsModal.includeNumber"),
                (value: string | undefined): boolean => {
                  if (value === undefined || value === "") {
                    return false;
                  }
                  const regex = /\d/u;

                  return regex.test(value);
                }
              )
              .test(
                "includeLowercase",
                translate.t("validations.credentialsModal.includeLowercase"),
                (value: string | undefined): boolean => {
                  if (value === undefined || value === "") {
                    return false;
                  }
                  const regex = /[a-z]/u;

                  return regex.test(value);
                }
              )
              .test(
                "includeUppercase",
                translate.t("validations.credentialsModal.includeUppercase"),
                (value: string | undefined): boolean => {
                  if (value === undefined || value === "") {
                    return false;
                  }
                  const regex = /[A-Z]/u;

                  return regex.test(value);
                }
              )
              .min(
                MIN_FIELD_LENGTH,
                translate.t("validations.minLength", {
                  count: MIN_FIELD_LENGTH,
                })
              )
              .max(
                MAX_FIELD_LENGTH,
                translate.t("validations.maxLength", {
                  count: MAX_FIELD_LENGTH,
                })
              )
              .test(
                "includeSymbols",
                translate.t("validations.credentialsModal.includeSymbols"),
                (value: string | undefined): boolean => {
                  if (value === undefined || value === "") {
                    return false;
                  }
                  const regex = /['~:;%@_$#!,.*\-?"[\]|()/{}>^<=&+`]/u;

                  return regex.test(value);
                }
              ),
          })
          .test(
            "hasValidValue",
            translate.t("validations.invalidSpaceField"),
            (value): boolean => {
              const regex = /\S/u;
              if (value === undefined) {
                return true;
              }

              return regex.test(value);
            }
          ),
        token: string()
          .when(["newSecrets", "type"], {
            is: (newSecrets: boolean, type: string): boolean =>
              newSecrets && type === (values.auth === "TOKEN" ? "HTTPS" : ""),
            otherwise: string(),
            then: string().required(translate.t("validations.required")),
          })
          .test(
            "hasValidValue",
            translate.t("validations.invalidSpaceField"),
            (value): boolean => {
              const regex = /\S/u;
              if (value === undefined) {
                return true;
              }

              return regex.test(value);
            }
          ),
        type: string().required(translate.t("validations.required")),
        user: string()
          .when(["newSecrets", "type"], {
            is: (newSecrets: boolean, type: string): boolean =>
              newSecrets && type === (values.auth === "USER" ? "HTTPS" : ""),
            otherwise: string(),
            then: string().required(translate.t("validations.required")),
          })
          .test(
            "hasValidValue",
            translate.t("validations.invalidSpaceField"),
            (value): boolean => {
              const regex = /\S/u;
              if (value === undefined) {
                return true;
              }

              return regex.test(value);
            }
          ),
      })
  );

export { validateSchema };
