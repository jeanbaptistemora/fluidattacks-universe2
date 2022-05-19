import { useMutation } from "@apollo/client";
import { faCircleInfo } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Field, Form, Formik } from "formik";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";
import { boolean, object, string } from "yup";

import { ADD_ORGANIZATION, GET_USER_WELCOME } from "../../queries";
import type { IAddOrganizationResult } from "../../types";
import { Button } from "components/Button";
import { Col, Row } from "components/Layout";
import { TooltipWrapper } from "components/TooltipWrapper";
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
    async (values: {
      groupDescription: string;
      groupName: string;
      organizationName: string;
      reportLanguage: string;
      termsOfservice: boolean;
    }): Promise<void> => {
      mixpanel.track("AddOrganization");
      await addOrganization({
        variables: { name: values.organizationName.toUpperCase() },
      });
      localStorage.clear();
      sessionStorage.clear();
      replace(`/orgs/${values.organizationName.toLowerCase()}/groups`);
    },
    [addOrganization, replace]
  );

  const minLenth = 4;
  const maxLength = 10;
  const validations = object().shape({
    groupDescription: string()
      .required()
      .min(minLenth)
      .max(maxLength)
      .matches(/^[a-zA-Z]+$/u),
    groupName: string().required(),
    organizationName: string().required(),
    reportLanguage: string().required(),
    termsOfservice: boolean().required(),
  });

  return (
    <div>
      <Formik
        enableReinitialize={true}
        initialValues={{
          groupDescription: "",
          groupName: "",
          organizationName: "",
          reportLanguage: "",
          termsOfservice: false,
        }}
        name={"newOrganization"}
        onSubmit={handleSubmit}
        validationSchema={validations}
      >
        <Form>
          <Row justify={"flex-start"}>
            <Col>
              <Row>
                <Col>
                  <strong>
                    {t("autoenrollment.addOrganization.organizationName")}
                  </strong>
                </Col>
                <Col>
                  <TooltipWrapper
                    id={"addGroupTooltip"}
                    message={t("sidebar.newOrganization.modal.nameTooltip")}
                    placement={"top"}
                  >
                    <FontAwesomeIcon icon={faCircleInfo} />
                  </TooltipWrapper>
                </Col>
              </Row>
              <Field
                component={FormikText}
                name={"organizationName"}
                type={"text"}
              />
            </Col>
          </Row>
          <Row justify={"flex-start"}>
            <Col>
              <Row>
                <Col>
                  <strong>
                    {t("autoenrollment.addOrganization.groupName")}
                  </strong>
                </Col>
                <Col>
                  <TooltipWrapper
                    id={"addGroupTooltip"}
                    message={t("sidebar.newOrganization.modal.nameTooltip")}
                    placement={"top"}
                  >
                    <FontAwesomeIcon icon={faCircleInfo} />
                  </TooltipWrapper>
                </Col>
              </Row>
              <Field component={FormikText} name={"groupName"} type={"text"} />
            </Col>
          </Row>
          <Row justify={"flex-start"}>
            <Col>
              <p>{t("autoenrollment.addOrganization.reportLanguageTip")}</p>
              <strong>
                {t("autoenrollment.addOrganization.reportLanguage")}
              </strong>
              <Field
                component={FormikText}
                name={"reportLanguage"}
                type={"text"}
              />
            </Col>
          </Row>
          <Row justify={"flex-start"}>
            <Col>
              <strong>
                {t("autoenrollment.addOrganization.groupDescription")}
              </strong>
              <Field
                component={FormikText}
                name={"groupDescription"}
                type={"text"}
              />
            </Col>
          </Row>
          <Row justify={"flex-start"}>
            <Col>
              <strong>{t("autoenrollment.addOrganization.roleTitle")}</strong>
              <p>{t("autoenrollment.addOrganization.role")}</p>
            </Col>
          </Row>
          <Row justify={"flex-start"}>
            <Col large={"10"} medium={"10"} small={"10"}>
              <Field
                component={FormikText}
                name={"termsOfService"}
                type={"checkbox"}
              />
            </Col>
            <Col large={"90"} medium={"90"} small={"90"}>
              {t("autoenrollment.addOrganization.termsOfService")}
            </Col>
          </Row>
          <Row justify={"center"}>
            <Col>
              <Button disabled={submitting} type={"submit"} variant={"primary"}>
                {t("autoenrollment.addOrganization.proceed")}
              </Button>
            </Col>
          </Row>
          <Row justify={"center"}>
            <Col>
              <Button onClick={goBack} variant={"secondary"}>
                {t("confirmmodal.cancel")}
              </Button>
            </Col>
          </Row>
        </Form>
      </Formik>
    </div>
  );
};

export { AddOrganization };
