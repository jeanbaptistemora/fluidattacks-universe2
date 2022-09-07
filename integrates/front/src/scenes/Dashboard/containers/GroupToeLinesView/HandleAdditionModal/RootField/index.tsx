/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { Field } from "formik";
import React from "react";

import type { IRootFieldProps } from "./types";

import type { IGitRootAttr } from "../types";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikDropdown } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import { required } from "utils/validations";

const RootField: React.FC<IRootFieldProps> = (
  props: IRootFieldProps
): JSX.Element => {
  const { roots } = props;

  return (
    <FormGroup>
      <ControlLabel>
        <b>{translate.t("group.toe.lines.addModal.fields.root")}</b>
      </ControlLabel>
      <Field
        component={FormikDropdown}
        name={"rootId"}
        type={"text"}
        validate={required}
      >
        {roots.map((root: IGitRootAttr): JSX.Element => {
          return (
            <option key={root.id} value={root.id}>
              {root.nickname}
            </option>
          );
        })}
      </Field>
    </FormGroup>
  );
};

export { RootField };
