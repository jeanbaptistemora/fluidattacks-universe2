import { Field } from "formik";
import React from "react";

import type { IRootFieldProps } from "./types";

import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikAutocompleteText } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import { composeValidators, required } from "utils/validations";

const RootField: React.FC<IRootFieldProps> = (
  props: IRootFieldProps
): JSX.Element => {
  const { roots } = props;
  const nicknames = roots.map((root): string => root.nickname);

  return (
    <FormGroup>
      <ControlLabel>
        {translate.t("group.toe.inputs.addModal.fields.root")}
      </ControlLabel>
      <Field
        component={FormikAutocompleteText}
        name={"rootNickname"}
        suggestions={nicknames}
        validate={composeValidators([required])}
      />
    </FormGroup>
  );
};

export { RootField };
