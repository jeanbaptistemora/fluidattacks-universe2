import { faMagnifyingGlass } from "@fortawesome/free-solid-svg-icons";
import { Form, Formik } from "formik";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { Input } from "components/Input";
import { alphaNumeric, composeValidators } from "utils/validations";

export const Searchbar: React.FC = (): JSX.Element => {
  const { push } = useHistory();
  const { t } = useTranslation();

  const handleSubmit = useCallback(
    (values: { groupName: string }): void => {
      const groupName = values.groupName.toLowerCase();
      if (groupName.trim() !== "") {
        mixpanel.track("SearchGroup", { group: groupName });
        push(`/groups/${groupName}/vulns`);
      }
    },
    [push]
  );

  return (
    <Container margin={"0 16px 0 0"}>
      <Formik
        initialValues={{ groupName: "" }}
        name={"searchBar"}
        onSubmit={handleSubmit}
      >
        <Form>
          <Input
            childLeft={
              <Button icon={faMagnifyingGlass} size={"xs"} type={"submit"} />
            }
            name={"groupName"}
            placeholder={t("navbar.searchPlaceholder")}
            validate={composeValidators([alphaNumeric])}
          />
        </Form>
      </Formik>
    </Container>
  );
};
