import { track } from "mixpanel-browser";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";
import { Field } from "redux-form";

import { GenericForm } from "../../GenericForm";
import { Text } from "utils/forms/fields";
import { alphaNumeric } from "utils/validations";

export const Searchbar: React.FC = (): JSX.Element => {
  const { push } = useHistory();
  const { t } = useTranslation();

  const handleSubmit = useCallback(
    (values: { projectName: string }): void => {
      const projectName = values.projectName.toLowerCase();
      if (projectName.trim() !== "") {
        track("SearchGroup", { group: projectName });
        push(`/groups/${projectName}/vulns`);
      }
    },
    [push]
  );

  return (
    <GenericForm name={"searchBar"} onSubmit={handleSubmit}>
      <Field
        component={Text}
        name={"projectName"}
        placeholder={t("navbar.searchPlaceholder")}
        validate={[alphaNumeric]}
      />
    </GenericForm>
  );
};
