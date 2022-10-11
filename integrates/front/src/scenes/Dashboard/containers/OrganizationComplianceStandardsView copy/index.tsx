/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import { Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";

import { GET_GROUP_UNFULFILLED_STANDARDS } from "./queries";
import type {
  IGroupAttr,
  IOrganizationComplianceStandardsProps,
  IUnfulfilledStandardAttr,
} from "./types";

import { Select } from "components/Input";
import { Col } from "components/Layout/Col";
import { Row } from "components/Layout/Row";
import { Text } from "components/Text";
import { GET_ORGANIZATION_GROUP_NAMES } from "scenes/Dashboard/components/Navbar/Breadcrumb/queries";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

const OrganizationComplianceStandardsView: React.FC<IOrganizationComplianceStandardsProps> =
  (props: IOrganizationComplianceStandardsProps): JSX.Element => {
    const { organizationId } = props;
    const { t } = useTranslation();

    // Handle state
    const [selectedGroupName, setSelectedGroupName] = useState<
      string | undefined
    >(undefined);

    // GraphQL queries
    const { data: groupsData } = useQuery<{
      organization: { groups: IGroupAttr[] };
    }>(GET_ORGANIZATION_GROUP_NAMES, {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning(
            "An error occurred loading organization group names",
            error
          );
        });
      },
      variables: {
        organizationId,
      },
    });
    const { data: unfulfilledStandardsData } = useQuery<{
      group: {
        compliance: { unfulfilledStandards: IUnfulfilledStandardAttr[] };
      };
    }>(GET_GROUP_UNFULFILLED_STANDARDS, {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning(
            "An error occurred loading group unfulfilled standards",
            error
          );
        });
      },
      skip: _.isUndefined(selectedGroupName) || _.isEmpty(selectedGroupName),
      variables: {
        groupName: selectedGroupName,
      },
    });

    // Format data
    const groups = useMemo(
      (): IGroupAttr[] =>
        _.isUndefined(groupsData) ? [] : groupsData.organization.groups,
      [groupsData]
    );
    const unfulfilledStandards = _.isUndefined(unfulfilledStandardsData)
      ? []
      : unfulfilledStandardsData.group.compliance.unfulfilledStandards;

    // Handle effects
    useEffect((): void => {
      if (_.isUndefined(selectedGroupName) && groups.length > 0) {
        setSelectedGroupName(groups[0].name);
      }
    }, [groups, selectedGroupName]);

    // Handle actions
    function onGroupChange(event: React.ChangeEvent<HTMLSelectElement>): void {
      event.preventDefault();
      setSelectedGroupName(event.target.value);
    }
    function onSubmit(): void {
      // OnSubmit
    }

    return (
      <React.StrictMode>
        <Row>
          <Col lg={50} md={50} sm={50}>
            <Formik
              initialValues={{
                groupName: selectedGroupName,
              }}
              name={"selectGroup"}
              onSubmit={onSubmit}
            >
              <div className={"flex flex-row  justify-start items-end "}>
                <div>
                  <Text disp={"inline"} fw={7} mb={3} mt={2} size={"big"}>
                    {t(
                      "organization.tabs.compliance.tabs.standards.unfulfilledStandards.title"
                    )}
                    {_.isUndefined(unfulfilledStandardsData)
                      ? undefined
                      : ` (${unfulfilledStandards.length})`}
                  </Text>
                </div>
                &emsp;
                <div>
                  <Select name={"groupName"} onChange={onGroupChange}>
                    {groups.map(
                      (group: IGroupAttr): JSX.Element => (
                        <option key={group.name} value={group.name}>
                          {_.startCase(group.name)}
                        </option>
                      )
                    )}
                  </Select>
                </div>
              </div>
            </Formik>
          </Col>
          <Col lg={50} md={50} sm={50}>
            <Row justify={"end"}>
              <div />
            </Row>
          </Col>
        </Row>
      </React.StrictMode>
    );
  };

export { OrganizationComplianceStandardsView };
