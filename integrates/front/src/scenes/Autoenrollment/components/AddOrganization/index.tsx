import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faCircleInfo } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";
import { array, object, string } from "yup";

import {
  ADD_GROUP_MUTATION,
  ADD_ORGANIZATION,
  GET_USER_WELCOME,
} from "../../queries";
import type { IAddOrganizationResult } from "../../types";
import { Button } from "components/Button";
import { Col, Row } from "components/Layout";
import { TooltipWrapper } from "components/TooltipWrapper";
import {
  FormikCheckbox,
  FormikDropdown,
  FormikText,
  FormikTextArea,
} from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const AddOrganization: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { goBack, replace } = useHistory();

  const [addOrganization, { loading: submittingOrg }] =
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

  const handleCreateError = ({ graphQLErrors }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      switch (error.message) {
        case "Exception - Error invalid group name":
          msgError(t("organization.tabs.groups.newGroup.invalidName"));
          break;
        case "Exception - User is not a member of the target organization":
          msgError(
            t("organization.tabs.groups.newGroup.userNotInOrganization")
          );
          break;
        default:
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred adding a group", error);
      }
    });
  };

  const [addGroup, { loading: submittingGroup }] = useMutation(
    ADD_GROUP_MUTATION,
    {
      onCompleted: (result: { addGroup: { success: boolean } }): void => {
        if (result.addGroup.success) {
          msgSuccess(
            t("organization.tabs.groups.newGroup.success"),
            t("organization.tabs.groups.newGroup.titleSuccess")
          );
        }
      },
      onError: handleCreateError,
    }
  );

  const handleSubmit = useCallback(
    async (values: {
      groupDescription: string;
      groupName: string;
      organizationName: string;
      reportLanguage: string;
      terms: string[];
    }): Promise<void> => {
      mixpanel.track("AddOrganization");
      await addOrganization({
        variables: { name: values.organizationName.toUpperCase() },
      });
      mixpanel.track("AddGroup");
      await addGroup({
        variables: {
          description: values.groupDescription,
          groupName: values.groupName.toUpperCase(),
          hasMachine: true,
          hasSquad: false,
          language: values.reportLanguage,
          organizationName: values.organizationName,
          service: "WHITE",
          subscription: "CONTINUOUS",
        },
      });
      localStorage.clear();
      sessionStorage.clear();
      replace(`/orgs/${values.organizationName.toLowerCase()}/groups`);
    },
    [addGroup, addOrganization, replace]
  );

  const minLenth = 4;
  const maxLength = 10;
  const validations = object().shape({
    groupDescription: string().required(),
    groupName: string().required(),
    organizationName: string()
      .required()
      .min(minLenth)
      .max(maxLength)
      .matches(/^[a-zA-Z]+$/u),
    reportLanguage: string().required(),
    terms: array().of(string()).required().length(1, t("validations.required")),
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
          terms: [],
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
                    {t("autoenrollment.addOrganization.organizationName.label")}
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
                placeholder={t(
                  "autoenrollment.addOrganization.organizationName.placeholder"
                )}
                type={"text"}
              />
            </Col>
          </Row>
          <Row justify={"flex-start"}>
            <Col>
              <Row>
                <Col>
                  <strong>
                    {t("autoenrollment.addOrganization.groupName.label")}
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
                name={"groupName"}
                placeholder={t(
                  "autoenrollment.addOrganization.groupName.placeholder"
                )}
                type={"text"}
              />
            </Col>
          </Row>
          <Row justify={"flex-start"}>
            <Col>
              <p>{t("autoenrollment.addOrganization.reportLanguageTip")}</p>
              <strong>
                {t("autoenrollment.addOrganization.reportLanguage")}
              </strong>
              <Field component={FormikDropdown} name={"reportLanguage"}>
                <option value={""}>{""}</option>
                <option value={"EN"}>
                  {t("organization.tabs.groups.newGroup.language.EN")}
                </option>
                <option value={"ES"}>
                  {t("organization.tabs.groups.newGroup.language.ES")}
                </option>
              </Field>
            </Col>
          </Row>
          <Row justify={"flex-start"}>
            <Col>
              <strong>
                {t("autoenrollment.addOrganization.groupDescription.label")}
              </strong>
              <Field
                component={FormikTextArea}
                name={"groupDescription"}
                placeholder={t(
                  "autoenrollment.addOrganization.groupDescription.placeholder"
                )}
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
          <Row justify={"center"}>
            <Col>
              <Field
                component={FormikCheckbox}
                label={t("autoenrollment.addOrganization.termsOfService")}
                name={"terms"}
                type={"checkbox"}
                value={"accept"}
              />
            </Col>
          </Row>
          <Row justify={"center"}>
            <Col>
              <Button
                disabled={submittingOrg || submittingGroup}
                type={"submit"}
                variant={"primary"}
              >
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
