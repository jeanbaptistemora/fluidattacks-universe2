import { faMagnifyingGlass } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Field, Form, Formik } from "formik";
import { track } from "mixpanel-browser";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";

import { SearchContainer, SearchInput } from "./styles";

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
        <SearchContainer>
          <FontAwesomeIcon icon={faMagnifyingGlass} />
          <Field
            component={SearchInput}
            name={"groupName"}
            placeholder={t("navbar.searchPlaceholder")}
            type={"text"}
            validate={composeValidators([alphaNumeric])}
          />
        </SearchContainer>
      </Form>
    </Formik>
  );
};
