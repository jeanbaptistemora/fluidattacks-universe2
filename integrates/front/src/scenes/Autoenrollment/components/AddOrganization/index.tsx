import { useMutation } from "@apollo/client";
import { Field, Form, Formik } from "formik";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";
import { object, string } from "yup";

import { ADD_ORGANIZATION, GET_USER_WELCOME } from "../../queries";
import type { IAddOrganizationResult } from "../../types";
import { Button } from "components/Button";
import { Col, Row } from "components/Layout";
import { TooltipWrapper } from "components/TooltipWrapper";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

const AddOrganization: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { goBack, replace } = useHistory();

  const [addOrganization, { loading: submitting }] =
    useMutation<IAddOrganizationResult>(ADD_ORGANIZATION, {
      awaitRefetchQueries: true,
      onCompleted: (result): void => {
        if (result.addOrganization.success) {
          mixpanel.track("NewOrganization", {
            OrganizationId: result.addOrganization.organization.id,
            OrganizationName: result.addOrganization.organization.name,
          });
        }
      },
      onError: (error): void => {
        error.graphQLErrors.forEach(({ message }): void => {
          if (message === "Access denied") {
            msgError(t("sidebar.newOrganization.modal.invalidName"));
          } else {
            Logger.error(
              "An error occurred creating new organization",
              message
            );
          }
        });
      },
      refetchQueries: [GET_USER_WELCOME],
    });

  const handleSubmit = useCallback(
    async (values: { name: string }): Promise<void> => {
      mixpanel.track("AddOrganization");
      await addOrganization({ variables: { name: values.name.toUpperCase() } });
      localStorage.clear();
      sessionStorage.clear();
      replace(`/orgs/${values.name.toLowerCase()}/groups`);
    },
    [addOrganization, replace]
  );

  const minLenth = 4;
  const maxLength = 10;
  const validations = object().shape({
    name: string()
      .required()
      .min(minLenth)
      .max(maxLength)
      .matches(/^[a-zA-Z]+$/u),
  });

  return (
    <div>
      <Formik
        enableReinitialize={true}
        initialValues={{ name: "" }}
        name={"newOrganization"}
        onSubmit={handleSubmit}
        validationSchema={validations}
      >
        <Form>
          <Row justify={"center"} key={0}>
            <Col large={"50"} medium={"50"} small={"50"}>
              <FormGroup>
                <ControlLabel>
                  {t("sidebar.newOrganization.modal.name")}
                </ControlLabel>
                <TooltipWrapper
                  id={"addOrgTooltip"}
                  message={t("sidebar.newOrganization.modal.nameTooltip")}
                  placement={"top"}
                >
                  <Field component={FormikText} name={"name"} type={"text"} />
                </TooltipWrapper>
              </FormGroup>
            </Col>
          </Row>
          <Button onClick={goBack} variant={"secondary"}>
            {t("confirmmodal.cancel")}
          </Button>
          <Button disabled={submitting} type={"submit"} variant={"primary"}>
            {t("confirmmodal.proceed")}
          </Button>
        </Form>
      </Formik>
    </div>
  );
};

export { AddOrganization };
