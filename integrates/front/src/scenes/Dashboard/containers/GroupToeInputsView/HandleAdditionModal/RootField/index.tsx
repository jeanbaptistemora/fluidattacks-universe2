import { Field } from "formik";
import React from "react";

import type { IRootFieldProps } from "./types";

import type { Root } from "../types";
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
        <b>{translate.t("group.toe.inputs.addModal.fields.root")}</b>
      </ControlLabel>
      <Field
        component={FormikDropdown}
        name={"rootId"}
        type={"text"}
        validate={required}
      >
        {roots.map((root: Root): JSX.Element => {
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
