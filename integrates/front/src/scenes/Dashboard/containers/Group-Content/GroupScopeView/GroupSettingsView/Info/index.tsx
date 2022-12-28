import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import dayjs from "dayjs";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";
import type { ConfigurableValidator } from "revalidate";

import { Button } from "components/Button";
import { Card } from "components/Card";
import { Select } from "components/Input";
import { Col, Row } from "components/Layout";
import { Text } from "components/Text";
import { Tooltip } from "components/Tooltip";
import {
  GET_GROUP_DATA,
  UPDATE_GROUP_INFO,
} from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/queries";
import { handleEditGroupDataError } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/Services/helpers";
import type { IGroupData } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/Services/types";
import { authzPermissionsContext } from "utils/authz/config";
import { formatIsoDate } from "utils/date";
import { FormikDate, FormikText } from "utils/forms/fields";
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
      value: string;
    }[]
  ): Record<string, string> => {
    return attributes.reduce(
      (
        acc: Record<string, string>,
        cur: {
          attribute: string;
          value: string;
        }
      ): Record<string, string> => ({
        ...acc,
        [attributeMapper(cur.attribute)]: cur.value,
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
    async (values: Record<string, string>): Promise<void> => {
      const isManagedChanged: boolean =
        data === undefined ? false : values.managed !== data.group.managed;
      await editGroupInfo({
        variables: {
          businessId: values.businessId,
          businessName: values.businessName,
          comments: "",
          description: values.description,
          groupName,
          isManagedChanged,
          language: values.language,
          managed: values.managed,
          sprintDuration: Number(values.sprintDuration),
          sprintStartDate: dayjs(values.sprintStartDate).toISOString(),
        },
      });
    },
    [data, editGroupInfo, groupName]
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
      value: data.group.managed,
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
        {({ dirty, isSubmitting }): JSX.Element => {
          return (
            <Form>
              <Row>
                <Col lg={33} md={50} sm={100}>
                  <Card>
                    <Text mb={2}>
                      {t("organization.tabs.groups.newGroup.businessId.text")}
                    </Text>
                    <Tooltip
                      id={
                        "organization.tabs.groups.newGroup.businessId.tooltip"
                      }
                      place={"top"}
                      tip={t(
                        "organization.tabs.groups.newGroup.businessId.tooltip"
                      )}
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
                    </Tooltip>
                  </Card>
                </Col>
                <Col lg={33} md={50} sm={100}>
                  <Card>
                    <Text mb={2}>
                      {t("organization.tabs.groups.newGroup.businessName.text")}
                    </Text>
                    <Tooltip
                      id={
                        "organization.tabs.groups.newGroup.businessName.tooltip"
                      }
                      place={"top"}
                      tip={t(
                        "organization.tabs.groups.newGroup.businessName.tooltip"
                      )}
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
                    </Tooltip>
                  </Card>
                </Col>
                <Col lg={33} md={50} sm={100}>
                  <Card>
                    <Text mb={2}>
                      {t("organization.tabs.groups.newGroup.description.text")}
                    </Text>
                    <Tooltip
                      id={
                        "organization.tabs.groups.newGroup.description.tooltip"
                      }
                      place={"top"}
                      tip={t(
                        "organization.tabs.groups.newGroup.description.tooltip"
                      )}
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
                    </Tooltip>
                  </Card>
                </Col>
                <Col lg={33} md={50} sm={100}>
                  <Card>
                    <Text mb={2}>
                      {t("organization.tabs.groups.newGroup.language.text")}
                    </Text>
                    <Tooltip
                      id={"organization.tabs.groups.newGroup.language.tooltip"}
                      place={"top"}
                      tip={t(
                        "organization.tabs.groups.newGroup.language.tooltip"
                      )}
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
                    </Tooltip>
                  </Card>
                </Col>
                <Col lg={33} md={50} sm={100}>
                  <Card>
                    <Text mb={2}>
                      {t(
                        "organization.tabs.groups.newGroup.sprintDuration.text"
                      )}
                    </Text>
                    <Tooltip
                      id={
                        "organization.tabs.groups.newGroup.sprintDuration.tooltip"
                      }
                      place={"top"}
                      tip={t(
                        "organization.tabs.groups.newGroup.sprintDuration.tooltip"
                      )}
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
                    </Tooltip>
                  </Card>
                </Col>
                <Col lg={33} md={50} sm={100}>
                  <Card>
                    <Text mb={2}>
                      {t(
                        "organization.tabs.groups.editGroup.sprintStartDate.text"
                      )}
                    </Text>
                    <Tooltip
                      id={
                        "organization.tabs.groups.editGroup.sprintStartDate.tooltip"
                      }
                      place={"top"}
                      tip={t(
                        "organization.tabs.groups.editGroup.sprintStartDate.tooltip"
                      )}
                    >
                      <Field
                        component={FormikDate}
                        disabled={permissions.cannot(
                          "api_mutations_update_group_stakeholder_mutate"
                        )}
                        name={"sprintStartDate"}
                        validate={composeValidators([required, isGreaterDate])}
                      />
                    </Tooltip>
                  </Card>
                </Col>
                <Col lg={33} md={50} sm={100}>
                  <Card>
                    <Text fw={7} mb={2}>
                      {t("organization.tabs.groups.newGroup.managed.text")}
                    </Text>
                    <Tooltip
                      id={"organization.tabs.groups.newGroup.managed.tooltip"}
                      place={"top"}
                      tip={t(
                        "organization.tabs.groups.newGroup.managed.tooltip"
                      )}
                    >
                      <Select
                        disabled={permissions.cannot(
                          "api_mutations_update_group_managed_mutate"
                        )}
                        name={"managed"}
                      >
                        <option value={"MANAGED"}>
                          {t(
                            "organization.tabs.groups.newGroup.managed.managed"
                          )}
                        </option>
                        <option value={"NOT_MANAGED"}>
                          {t(
                            "organization.tabs.groups.newGroup.managed.notManaged"
                          )}
                        </option>
                        <option value={"UNDER_REVIEW"}>
                          {t(
                            "organization.tabs.groups.newGroup.managed.underReview"
                          )}
                        </option>
                        <option value={"TRIAL"}>
                          {t("organization.tabs.groups.newGroup.managed.trial")}
                        </option>
                      </Select>
                    </Tooltip>
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
