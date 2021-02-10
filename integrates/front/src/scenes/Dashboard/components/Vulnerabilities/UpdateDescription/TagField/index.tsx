import { Field } from "redux-form";
import type { ITagFieldProps } from "./types";
import React from "react";
import { TagInput } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import { ControlLabel, FormGroup } from "styles/styledComponents";

const TagField: React.FC<ITagFieldProps> = (
  props: ITagFieldProps
): JSX.Element => {
  const {
    handleDeletion,
    hasNewVulnSelected,
    isAcceptedSelected,
    isAcceptedUndefinedSelected,
    isInProgressSelected,
  } = props;

  return (
    <React.StrictMode>
      {isAcceptedSelected ||
      isAcceptedUndefinedSelected ||
      isInProgressSelected ||
      !hasNewVulnSelected ? (
        <FormGroup>
          <ControlLabel>
            <b>{translate.t("search_findings.tab_description.tag")}</b>
          </ControlLabel>
          <Field
            component={TagInput}
            name={"tag"}
            onDeletion={handleDeletion}
            type={"text"}
          />
        </FormGroup>
      ) : undefined}
    </React.StrictMode>
  );
};

export { TagField };
