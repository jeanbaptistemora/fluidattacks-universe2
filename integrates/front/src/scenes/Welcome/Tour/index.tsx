import { useMutation, useQuery } from "@apollo/client";
import { Field, Form, Formik } from "formik";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";

import { ADD_ORGANIZATION, GET_NEW_ORGANIZATION_NAME } from "../queries";
import type {
  IAddOrganizationResult,
  IGetNewOrganizationNameResult,
} from "../types";
import { Button } from "components/Button";
import { Col, Row } from "components/Layout";
import { TooltipWrapper } from "components/TooltipWrapper";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

const Tour: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { goBack, replace } = useHistory();

  const { data, loading } = useQuery<IGetNewOrganizationNameResult>(
    GET_NEW_ORGANIZATION_NAME,
    {
      fetchPolicy: "no-cache",
      onError: (error): void => {
        error.graphQLErrors.forEach(({ message }): void => {
          if (
            message ===
            "Exception - There are no organization names available at the moment"
          ) {
            msgError(t("sidebar.newOrganization.modal.namesUnavailable"));
          } else {
            msgError(t("groupAlerts.errorTextsad"));
            Logger.warning(
              "An error occurred getting a name for a new organization",
              message
            );
          }
        });
      },
    }
  );
  const organizationName =
    data === undefined ? "" : data.internalNames.name.toUpperCase();

  const [addOrganization, { loading: submitting }] =
    useMutation<IAddOrganizationResult>(ADD_ORGANIZATION, {
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
            msgError(t("groupAlerts.errorTextsad"));
            Logger.warning(
              "An error occurred creating new organization",
              message
            );
          }
        });
      },
    });

  const handleSubmit = useCallback(
    async (values: { name: string }): Promise<void> => {
      mixpanel.track("AddOrganization");
      await addOrganization({ variables: values });
      replace(`/orgs/${values.name}/groups`);
    },
    [addOrganization, replace]
  );

  return (
    <div>
      <Formik
        enableReinitialize={true}
        initialValues={{ name: organizationName }}
        name={"newOrganization"}
        onSubmit={handleSubmit}
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
                  <Field
                    component={FormikText}
                    disabled={true}
                    name={"name"}
                    type={"text"}
                  />
                </TooltipWrapper>
              </FormGroup>
            </Col>
          </Row>
          <Button onClick={goBack} variant={"secondary"}>
            {t("confirmmodal.cancel")}
          </Button>
          <Button
            disabled={loading || submitting}
            type={"submit"}
            variant={"primary"}
          >
            {t("confirmmodal.proceed")}
          </Button>
        </Form>
      </Formik>
    </div>
  );
};

export { Tour };
