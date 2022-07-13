import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import moment from "moment";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";
import type { ConfigurableValidator } from "revalidate";

import { Button } from "components/Button";
import { Card } from "components/Card";
import { Select } from "components/Input";
import { Col, Row } from "components/Layout";
import { Text } from "components/Text";
import { TooltipWrapper } from "components/TooltipWrapper";
import {
  GET_GROUP_DATA,
  UPDATE_GROUP_INFO,
} from "scenes/Dashboard/containers/GroupSettingsView/queries";
import { handleEditGroupDataError } from "scenes/Dashboard/containers/GroupSettingsView/Services/helpers";
import type { IGroupData } from "scenes/Dashboard/containers/GroupSettingsView/Services/types";
import { authzPermissionsContext } from "utils/authz/config";
import { formatIsoDate } from "utils/date";
import { FormikDate, FormikText } from "utils/forms/fields";
import { FormikSwitchButton } from "utils/forms/fields/SwitchButton/FormikSwitchButton";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import {
  composeValidators,
  isGreaterDate,
  maxLength,
  numberBetween,
  numeric,
  required,
  validTextField,
} from "utils/validations";

const MAX_BUSINESS_INFO_LENGTH: number = 60;
const MAX_DESCRIPTION_LENGTH: number = 200;
const MIN_SPRINT_DURATION: number = 1;
const MAX_SPRINT_DURATION: number = 10;

const maxBusinessInfoLength: ConfigurableValidator = maxLength(
  MAX_BUSINESS_INFO_LENGTH
);
const maxDescriptionLength: ConfigurableValidator = maxLength(
  MAX_DESCRIPTION_LENGTH
);

const GroupInformation: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const { t } = useTranslation();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);

  const attributeMapper = (attribute: string): string => {
    /**
     * Needed for the new attribute headers of the dataset that do not match
     * the underlying field names
     */
    if (attribute === "Business Registration Number") {
      return "businessId";
    } else if (attribute === "Business Name") {
      return "businessName";
    } else if (attribute === "Sprint Length") {
      return "sprintDuration";
    } else if (attribute === "Sprint Start Date") {
      return "sprintStartDate";
    } else if (attribute === "Managed") {
      return "managed";
    }

    return attribute.toLocaleLowerCase();
  };

  const formatDataSet = (
    attributes: {
      attribute: string;
      value: boolean | string;
    }[]
  ): Record<string, boolean | string> => {
    return attributes.reduce(
      (
        acc: Record<string, boolean | string>,
        cur: {
          attribute: string;
          value: boolean | string;
        }
      ): Record<string, boolean | string> => ({
        ...acc,
        [attributeMapper(cur.attribute)]:
          cur.attribute === "Managed" ? cur.value === "Manually" : cur.value,
      }),
      {}
    );
  };

  const {
    data,
    loading: loadingGroupData,
    refetch: refetchGroupData,
  } = useQuery<IGroupData>(GET_GROUP_DATA, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorText"));
        Logger.warning("An error occurred getting group data", error);
      });
    },
    variables: { groupName },
  });

  const [editGroupInfo] = useMutation(UPDATE_GROUP_INFO, {
    onCompleted: async (): Promise<void> => {
      mixpanel.track("EditGroupData");
      msgSuccess(
        t("groupAlerts.groupInfoUpdated"),
        t("groupAlerts.titleSuccess")
      );
      await refetchGroupData({ groupName });
    },
    onError: (error: ApolloError): void => {
      handleEditGroupDataError(error);
    },
  });

  const handleFormSubmit = useCallback(
    async (values: Record<string, boolean | string>): Promise<void> => {
      await editGroupInfo({
        variables: {
          businessId: values.businessId,
          businessName: values.businessName,
          comments: "",
          description: values.description,
          groupName,
          language: values.language,
          managed: values.managed === true ? "MANUALLY" : "NOT_MANUALLY",
          sprintDuration: Number(values.sprintDuration),
          sprintStartDate: moment(
            values.sprintStartDate as string
          ).toISOString(),
        },
      });
    },
    [editGroupInfo, groupName]
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }
  const attributesDataset: {
    attribute: string;
    value: string;
  }[] = [
    {
      attribute: "Language",
      value: data.group.language,
    },
    {
      attribute: "Description",
      value: data.group.description,
    },
    {
      attribute: "Business Registration Number",
      value: data.group.businessId,
    },
    {
      attribute: "Business Name",
      value: data.group.businessName,
    },
    {
      attribute: "Managed",
      value:
        data.group.managed === "MANUALLY"
          ? t("organization.tabs.groups.newGroup.managed.manually")
          : t("organization.tabs.groups.newGroup.managed.notManually"),
    },
    {
      attribute: "Sprint Length",
      value: data.group.sprintDuration,
    },
    {
      attribute: "Sprint Start Date",
      value: formatIsoDate(data.group.sprintStartDate),
    },
  ];

  return (
    <React.StrictMode>
      <Formik
        enableReinitialize={true}
        initialValues={formatDataSet(attributesDataset)}
        name={"editGroupInformation"}
        onSubmit={handleFormSubmit}
      >
        {({ dirty, isSubmitting, setFieldValue }): JSX.Element => {
          function managedOnChange(managed: boolean): void {
            setFieldValue("managed", managed);
          }

          return (
            <Form>
              <Row>
                <Col large={"33"} medium={"50"} small={"100"}>
                  <Card>
                    <Text mb={2}>
                      {t("organization.tabs.groups.newGroup.businessId.text")}
                    </Text>
                    <TooltipWrapper
                      id={
                        "organization.tabs.groups.newGroup.businessId.tooltip"
                      }
                      message={t(
                        "organization.tabs.groups.newGroup.businessId.tooltip"
                      )}
                      placement={"top"}
                    >
                      <Field
                        component={FormikText}
                        disabled={permissions.cannot(
                          "api_mutations_update_group_stakeholder_mutate"
                        )}
                        id={"add-group-description"}
                        name={"businessId"}
                        type={"text"}
                        validate={composeValidators([
                          maxBusinessInfoLength,
                          validTextField,
                        ])}
                      />
                    </TooltipWrapper>
                  </Card>
                </Col>
                <Col large={"33"} medium={"50"} small={"100"}>
                  <Card>
                    <Text mb={2}>
                      {t("organization.tabs.groups.newGroup.businessName.text")}
                    </Text>
                    <TooltipWrapper
                      id={
                        "organization.tabs.groups.newGroup.businessName.tooltip"
                      }
                      message={t(
                        "organization.tabs.groups.newGroup.businessName.tooltip"
                      )}
                      placement={"top"}
                    >
                      <Field
                        component={FormikText}
                        disabled={permissions.cannot(
                          "api_mutations_update_group_stakeholder_mutate"
                        )}
                        id={"add-group-description"}
                        name={"businessName"}
                        type={"text"}
                        validate={composeValidators([
                          maxBusinessInfoLength,
                          validTextField,
                        ])}
                      />
                    </TooltipWrapper>
                  </Card>
                </Col>
                <Col large={"33"} medium={"50"} small={"100"}>
                  <Card>
                    <Text mb={2}>
                      {t("organization.tabs.groups.newGroup.description.text")}
                    </Text>
                    <TooltipWrapper
                      id={
                        "organization.tabs.groups.newGroup.description.tooltip"
                      }
                      message={t(
                        "organization.tabs.groups.newGroup.description.tooltip"
                      )}
                      placement={"top"}
                    >
                      <Field
                        component={FormikText}
                        disabled={permissions.cannot(
                          "api_mutations_update_group_stakeholder_mutate"
                        )}
                        id={"add-group-description"}
                        name={"description"}
                        type={"text"}
                        validate={composeValidators([
                          required,
                          maxDescriptionLength,
                          validTextField,
                        ])}
                      />
                    </TooltipWrapper>
                  </Card>
                </Col>
                <Col large={"33"} medium={"50"} small={"100"}>
                  <Card>
                    <Text mb={2}>
                      {t("organization.tabs.groups.newGroup.language.text")}
                    </Text>
                    <TooltipWrapper
                      id={"organization.tabs.groups.newGroup.language.tooltip"}
                      message={t(
                        "organization.tabs.groups.newGroup.language.tooltip"
                      )}
                      placement={"top"}
                    >
                      <Select
                        disabled={permissions.cannot(
                          "api_mutations_update_group_stakeholder_mutate"
                        )}
                        name={"language"}
                      >
                        <option value={"EN"}>
                          {t("organization.tabs.groups.newGroup.language.EN")}
                        </option>
                        <option value={"ES"}>
                          {t("organization.tabs.groups.newGroup.language.ES")}
                        </option>
                      </Select>
                    </TooltipWrapper>
                  </Card>
                </Col>
                <Col large={"33"} medium={"50"} small={"100"}>
                  <Card>
                    <Text mb={2}>
                      {t(
                        "organization.tabs.groups.newGroup.sprintDuration.text"
                      )}
                    </Text>
                    <TooltipWrapper
                      id={
                        "organization.tabs.groups.newGroup.sprintDuration.tooltip"
                      }
                      message={t(
                        "organization.tabs.groups.newGroup.sprintDuration.tooltip"
                      )}
                      placement={"top"}
                    >
                      <Field
                        component={FormikText}
                        disabled={permissions.cannot(
                          "api_mutations_update_group_stakeholder_mutate"
                        )}
                        id={"add-group-description"}
                        name={"sprintDuration"}
                        type={"text"}
                        validate={composeValidators([
                          numberBetween(
                            MIN_SPRINT_DURATION,
                            MAX_SPRINT_DURATION
                          ),
                          numeric,
                        ])}
                      />
                    </TooltipWrapper>
                  </Card>
                </Col>
                <Col large={"33"} medium={"50"} small={"100"}>
                  <Card>
                    <Text mb={2}>
                      {t(
                        "organization.tabs.groups.editGroup.sprintStartDate.text"
                      )}
                    </Text>
                    <TooltipWrapper
                      id={
                        "organization.tabs.groups.editGroup.sprintStartDate.tooltip"
                      }
                      message={t(
                        "organization.tabs.groups.editGroup.sprintStartDate.tooltip"
                      )}
                      placement={"top"}
                    >
                      <Field
                        component={FormikDate}
                        disabled={permissions.cannot(
                          "api_mutations_update_group_stakeholder_mutate"
                        )}
                        name={"sprintStartDate"}
                        validate={composeValidators([required, isGreaterDate])}
                      />
                    </TooltipWrapper>
                  </Card>
                </Col>
                <Col large={"33"} medium={"50"} small={"100"}>
                  <Card>
                    <Text mb={2}>
                      {t("organization.tabs.groups.newGroup.managed.text")}
                    </Text>
                    <TooltipWrapper
                      id={"organization.tabs.groups.newGroup.managed.tooltip"}
                      message={t(
                        "organization.tabs.groups.newGroup.managed.tooltip"
                      )}
                      placement={"top"}
                    >
                      <Field
                        component={FormikSwitchButton}
                        disabled={permissions.cannot(
                          "api_mutations_update_group_stakeholder_mutate"
                        )}
                        name={"managed"}
                        offlabel={t(
                          "organization.tabs.groups.newGroup.managed.notManually"
                        )}
                        onChange={managedOnChange}
                        onlabel={t(
                          "organization.tabs.groups.newGroup.managed.manually"
                        )}
                        type={"checkbox"}
                      />
                    </TooltipWrapper>
                  </Card>
                </Col>
              </Row>
              <div className={"mt2"} />
              {!dirty || loadingGroupData || isSubmitting ? undefined : (
                <Button type={"submit"} variant={"secondary"}>
                  {t("searchFindings.servicesTable.modal.continue")}
                </Button>
              )}
            </Form>
          );
        }}
      </Formik>
    </React.StrictMode>
  );
};

export { GroupInformation };
