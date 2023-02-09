import { useFormikContext } from "formik";
import _ from "lodash";
import React from "react";

import type { IEnvironmentUrlFieldProps } from "./types";

import type { IFormValues } from "../types";
import { isGitRoot } from "../utils";
import { Select } from "components/Input";
import { FormGroup } from "styles/styledComponents";
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
    !_.isEmpty(environmentUrlValue) &&
    (_.isUndefined(selectedRoot) ||
      !isGitRoot(selectedRoot) ||
      (!_.isUndefined(selectedRoot) &&
        isGitRoot(selectedRoot) &&
        _.isEmpty(selectedRoot.gitEnvironmentUrls)))
  ) {
    setFieldValue("environmentUrl", "");
  }
  if (
    _.isEmpty(environmentUrlValue) &&
    !_.isUndefined(selectedRoot) &&
    isGitRoot(selectedRoot) &&
    !_.isEmpty(selectedRoot.gitEnvironmentUrls)
  ) {
    setFieldValue("environmentUrl", selectedRoot.gitEnvironmentUrls[0].url);
  }

  return (
    <FormGroup>
      {!_.isUndefined(selectedRoot) && isGitRoot(selectedRoot) ? (
        <Select
          id={"environmentUrl"}
          label={translate.t("group.toe.inputs.addModal.fields.environmentUrl")}
          name={"environmentUrl"}
          validate={required}
        >
          <option value={""}>{""}</option>
          {selectedRoot.gitEnvironmentUrls.map(
            (envUrl): JSX.Element => (
              <option key={envUrl.id} value={envUrl.url}>
                {envUrl.url}
              </option>
            )
          )}
        </Select>
      ) : undefined}
    </FormGroup>
  );
};

export { EnvironmentUrlField };
