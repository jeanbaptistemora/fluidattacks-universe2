import { Field, useFormikContext } from "formik";
import _ from "lodash";
import React from "react";

import type { IEnvironmentUrlFieldProps } from "./types";

import type { IFormValues } from "../types";
import { isGitRoot } from "../utils";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikAutocompleteText } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import {
  composeValidators,
  isValidEnvironmentUrl,
  required,
} from "utils/validations";

const EnvironmentUrlField: React.FC<IEnvironmentUrlFieldProps> = (
  props: IEnvironmentUrlFieldProps
): JSX.Element => {
  const { selectedRoot } = props;
  const {
    values: { environmentUrl: environmentUrlValue },
    setFieldValue,
  } = useFormikContext<IFormValues>();
  if (
    !_.isEmpty(environmentUrlValue) &&
    (_.isUndefined(selectedRoot) ||
      !isGitRoot(selectedRoot) ||
      (!_.isUndefined(selectedRoot) &&
        isGitRoot(selectedRoot) &&
        _.isEmpty(selectedRoot.environmentUrls)))
  ) {
    setFieldValue("environmentUrl", "");
  }
  if (
    _.isEmpty(environmentUrlValue) &&
    !_.isUndefined(selectedRoot) &&
    isGitRoot(selectedRoot) &&
    !_.isEmpty(selectedRoot.environmentUrls)
  ) {
    setFieldValue("environmentUrl", selectedRoot.environmentUrls[0]);
  }

  return (
    <FormGroup>
      {!_.isUndefined(selectedRoot) && isGitRoot(selectedRoot) ? (
        <React.Fragment>
          <ControlLabel>
            <b>
              {translate.t("group.toe.inputs.addModal.fields.environmentUrl")}
            </b>
          </ControlLabel>

          <Field
            alignField={"horizontal"}
            component={FormikAutocompleteText}
            focus={true}
            id={"environmentUrl"}
            key={`environmentUrl-${selectedRoot.id}`}
            name={"environmentUrl"}
            renderAsEditable={false}
            suggestions={selectedRoot.environmentUrls}
            type={"text"}
            validate={composeValidators([
              isValidEnvironmentUrl(selectedRoot.environmentUrls),
              required,
            ])}
          />
        </React.Fragment>
      ) : undefined}
    </FormGroup>
  );
};

export { EnvironmentUrlField };
