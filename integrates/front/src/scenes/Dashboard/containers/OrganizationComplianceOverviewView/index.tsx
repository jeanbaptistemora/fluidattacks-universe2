/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import { PercentageCard } from "./PercentageCard";
import { GET_ORGANIZATION_COMPLIANCE } from "./queries";
import type {
  IOrganizationAttr,
  IOrganizationComplianceOverviewProps,
} from "./types";

import { InfoDropdown } from "components/InfoDropdown";
import { Col } from "components/Layout/Col";
import { Row } from "components/Layout/Row";
import { Text } from "components/Text";
import { Logger } from "utils/logger";

const handleComplianceValue: (value: number | null) => number = (
  value: number | null
  // eslint-disable-next-line @typescript-eslint/no-magic-numbers
): number => (_.isNull(value) ? 0 : value * 100);

const OrganizationComplianceOverviewView: React.FC<IOrganizationComplianceOverviewProps> =
  ({ organizationId }: IOrganizationComplianceOverviewProps): JSX.Element => {
    const { t } = useTranslation();

    // GraphQl queries
    const { data } = useQuery<{
      organization: IOrganizationAttr;
    }>(GET_ORGANIZATION_COMPLIANCE, {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          Logger.error("Couldn't load organization compliance", error);
        });
      },
      variables: {
        organizationId,
      },
    });

    if (_.isUndefined(data)) {
      return <div />;
    }
    const { organization } = data;

    return (
      <React.StrictMode>
        <Row>
          <Col lg={60} md={60} sm={100}>
            <Text fw={7} mb={3} mt={4} size={5}>
              {t(
                "organization.tabs.compliance.tabs.overview.nonCompliance.title.text",
                {
                  percentage: handleComplianceValue(
                    organization.compliance.nonComplianceLevel
                  ),
                }
              )}{" "}
              <InfoDropdown>
                <Text size={2} ta={"center"}>
                  {t(
                    "organization.tabs.compliance.tabs.overview.nonCompliance.title.info",
                    { organizationName: organization.name }
                  )}
                </Text>
              </InfoDropdown>
            </Text>
            <Col lg={33} md={33} sm={33}>
              <PercentageCard
                info={t(
                  "organization.tabs.compliance.tabs.overview.nonCompliance.complianceLevel.info",
                  {
                    percentage: handleComplianceValue(
                      organization.compliance.nonComplianceLevel
                    ),
                  }
                )}
                percentage={handleComplianceValue(
                  organization.compliance.nonComplianceLevel
                )}
                title={t(
                  "organization.tabs.compliance.tabs.overview.nonCompliance.complianceLevel.title",
                  { organizationName: organization.name }
                )}
              />
            </Col>
          </Col>
          <Col lg={40} md={40} sm={100} />
        </Row>
      </React.StrictMode>
    );
  };

export { OrganizationComplianceOverviewView };
