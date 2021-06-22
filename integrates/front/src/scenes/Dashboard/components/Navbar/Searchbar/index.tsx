import { Field, Form, Formik } from "formik";
import { track } from "mixpanel-browser";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";

import { FormikText } from "utils/forms/fields";
import { alphaNumeric, composeValidators } from "utils/validations";

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
    <Formik
      initialValues={{ projectName: "" }}
      name={"searchBar"}
      onSubmit={handleSubmit}
    >
      <Form>
        <Field
          component={FormikText}
          name={"projectName"}
          placeholder={t("navbar.searchPlaceholder")}
          validate={composeValidators([alphaNumeric])}
        />
      </Form>
    </Formik>
  );
};
