/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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
