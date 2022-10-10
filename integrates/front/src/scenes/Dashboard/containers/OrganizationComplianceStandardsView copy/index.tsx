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
import React from "react";
import { useTranslation } from "react-i18next";

import type {
  IGroupAttr,
  IOrganizationComplianceStandardsProps,
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
    const groups = _.isUndefined(groupsData)
      ? []
      : groupsData.organization.groups;

    function onSubmit(): void {
      // OnSubmit
    }

    return (
      <React.StrictMode>
        <Row>
          <Col lg={50} md={50} sm={50}>
            <Formik
              initialValues={{
                groupName: "",
              }}
              name={"selectGroup"}
              onSubmit={onSubmit}
            >
              <div className={"flex flex-row  justify-start"}>
                <div>
                  <Text disp={"inline"} fw={7} mb={3} mt={2} size={"big"}>
                    {t(
                      "organization.tabs.compliance.tabs.standards.unfulfilledStandards.title"
                    )}
                  </Text>
                </div>
                &emsp;
                <div>
                  <Select name={"groupName"}>
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
