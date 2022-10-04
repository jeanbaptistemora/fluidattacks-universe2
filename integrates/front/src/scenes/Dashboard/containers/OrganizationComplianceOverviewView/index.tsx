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

import { BenchmarkCard } from "./BenchmarkCard";
import { DaysCard } from "./DaysCard";
import { PercentageCard } from "./PercentageCard";
import { GET_ORGANIZATION_COMPLIANCE } from "./queries";
import { TrendCard } from "./TrendCard";
import type {
  IOrganizationAttr,
  IOrganizationComplianceOverviewProps,
  IStandardComplianceAttr,
} from "./types";
import {
  handleCompliancePercentageValue,
  handleComplianceValue,
} from "./utils";

import { InfoDropdown } from "components/InfoDropdown";
import { Col } from "components/Layout/Col";
import { Row } from "components/Layout/Row";
import { Text } from "components/Text";
import { Logger } from "utils/logger";

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
            <Text fw={7} mb={3} mt={2} size={"big"}>
              {t(
                "organization.tabs.compliance.tabs.overview.organizationCompliance.title.text"
              )}{" "}
              <InfoDropdown>
                <Text size={"small"} ta={"center"}>
                  {t(
                    "organization.tabs.compliance.tabs.overview.organizationCompliance.title.info",
                    { organizationName: organization.name }
                  )}
                </Text>
              </InfoDropdown>
            </Text>
            <Row>
              <Col lg={33} md={33} sm={33}>
                <PercentageCard
                  info={t(
                    "organization.tabs.compliance.tabs.overview.organizationCompliance.complianceLevel.info",
                    {
                      percentage: handleCompliancePercentageValue(
                        organization.compliance.complianceLevel
                      ),
                    }
                  )}
                  percentage={handleCompliancePercentageValue(
                    organization.compliance.complianceLevel
                  )}
                  title={t(
                    "organization.tabs.compliance.tabs.overview.organizationCompliance.complianceLevel.title",
                    { organizationName: organization.name }
                  )}
                />
              </Col>
              <Col lg={33} md={33} sm={33}>
                <TrendCard
                  info={t(
                    "organization.tabs.compliance.tabs.overview.organizationCompliance.complianceWeeklyTrend.info",
                    {
                      percentage: handleCompliancePercentageValue(
                        organization.compliance.complianceWeeklyTrend
                      ),
                    }
                  )}
                  title={t(
                    "organization.tabs.compliance.tabs.overview.organizationCompliance.complianceWeeklyTrend.title"
                  )}
                  trend={handleComplianceValue(
                    organization.compliance.complianceWeeklyTrend
                  )}
                />
              </Col>
              <Col lg={33} md={33} sm={33}>
                <DaysCard
                  days={handleComplianceValue(
                    organization.compliance.estimatedDaysToFullCompliance
                  )}
                  info={t(
                    "organization.tabs.compliance.tabs.overview.organizationCompliance.etToFullCompliance.info",
                    {
                      days: organization.compliance
                        .estimatedDaysToFullCompliance,
                    }
                  )}
                  title={t(
                    "organization.tabs.compliance.tabs.overview.organizationCompliance.etToFullCompliance.title"
                  )}
                />
              </Col>
            </Row>
          </Col>
          <Col lg={40} md={40} sm={100}>
            <Text fw={7} mb={3} mt={2} size={"big"}>
              {t(
                "organization.tabs.compliance.tabs.overview.standardWithLowestCompliance.title.text"
              )}{" "}
              <InfoDropdown>
                <Text size={"small"} ta={"center"}>
                  {t(
                    "organization.tabs.compliance.tabs.overview.standardWithLowestCompliance.title.info",
                    { organizationName: organization.name }
                  )}
                </Text>
              </InfoDropdown>
            </Text>
          </Col>
        </Row>
        <Row>
          <Col lg={100} md={100} sm={100}>
            <Text fw={7} mb={3} mt={2} size={"big"}>
              {t("organization.tabs.compliance.tabs.overview.benchmark.title")}
            </Text>
            <Row>
              {_.sortBy(
                organization.compliance.standards,
                (standardCompliance: IStandardComplianceAttr): string =>
                  standardCompliance.standardTitle.toUpperCase()
              ).map(
                (standardCompliance: IStandardComplianceAttr): JSX.Element => (
                  <Col
                    key={standardCompliance.standardTitle}
                    lg={25}
                    md={50}
                    sm={100}
                  >
                    <BenchmarkCard standardCompliance={standardCompliance} />
                  </Col>
                )
              )}
            </Row>
          </Col>
        </Row>
      </React.StrictMode>
    );
  };

export { OrganizationComplianceOverviewView };
