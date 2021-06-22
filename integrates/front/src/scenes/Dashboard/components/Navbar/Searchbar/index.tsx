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
    (values: { groupName: string }): void => {
      const groupName = values.groupName.toLowerCase();
      if (groupName.trim() !== "") {
        track("SearchGroup", { group: groupName });
        push(`/groups/${groupName}/vulns`);
      }
    },
    [push]
  );

  return (
    <Formik
      initialValues={{ groupName: "" }}
      name={"searchBar"}
      onSubmit={handleSubmit}
    >
      <Form>
        <Field
          component={FormikText}
          name={"groupName"}
          placeholder={t("navbar.searchPlaceholder")}
          validate={composeValidators([alphaNumeric])}
        />
      </Form>
    </Formik>
  );
};
