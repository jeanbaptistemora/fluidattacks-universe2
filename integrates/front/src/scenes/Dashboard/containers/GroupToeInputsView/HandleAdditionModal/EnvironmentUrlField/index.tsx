import { Field, useFormikContext } from "formik";
import _ from "lodash";
import React from "react";

import type { IEnvironmentUrlFieldProps } from "./types";

import type { IFormValues } from "../types";
import { isGitRoot } from "../utils";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikDropdown } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import { required } from "utils/validations";

const EnvironmentUrlField: React.FC<IEnvironmentUrlFieldProps> = (
  props: IEnvironmentUrlFieldProps
): JSX.Element => {
  const { selectedRoot } = props;
  const {
    values: { environmentUrl: environmentUrlValue },
    setFieldValue,
  } = useFormikContext<IFormValues>();
  if (
    !_.isUndefined(environmentUrlValue) &&
    (_.isUndefined(selectedRoot) ||
      !isGitRoot(selectedRoot) ||
      (!_.isUndefined(selectedRoot) &&
        isGitRoot(selectedRoot) &&
        _.isEmpty(selectedRoot.environmentUrls)))
  ) {
    setFieldValue("environmentUrl", undefined);
  }
  if (
    _.isUndefined(environmentUrlValue) &&
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
            component={FormikDropdown}
            name={"environmentUrl"}
            type={"text"}
            validate={required}
          >
            {selectedRoot.environmentUrls.map(
              (environmentUrl: string): JSX.Element => (
                <option key={environmentUrl} value={environmentUrl}>
                  {environmentUrl}
                </option>
              )
            )}
          </Field>
        </React.Fragment>
      ) : undefined}
    </FormGroup>
  );
};

export { EnvironmentUrlField };
