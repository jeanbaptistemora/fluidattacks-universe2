/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { FC } from "react";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IStandardComplianceAttr } from "../types";
import { getProgressBarColor, handleComplianceValue } from "../utils";
import { Card } from "components/Card";
import { Col } from "components/Layout/Col";
import { Row } from "components/Layout/Row";
import { ProgressBar } from "components/ProgressBar";
import { Text } from "components/Text";

interface IBenchmarkCardProps {
  standardCompliance: IStandardComplianceAttr;
}

const BenchmarkCard: FC<IBenchmarkCardProps> = (
  props: IBenchmarkCardProps
): JSX.Element => {
  const { standardCompliance } = props;
  const { t } = useTranslation();

  return (
    <Card>
      <Row>
        <Text fw={6} size={3} ta={"center"}>
          {standardCompliance.standardTitle}
        </Text>
      </Row>
      <br />
      <Row>
        <Col lg={50} md={50} sm={50}>
          <Text ta={"start"}>
            {t(
              "organization.tabs.compliance.tabs.overview.benchmark.myOrganization"
            )}
          </Text>
        </Col>
        <Col lg={50} md={50} sm={50}>
          <Text ta={"end"}>
            {`${handleComplianceValue(standardCompliance.nonComplianceLevel)}%`}{" "}
            <ProgressBar
              height={10}
              maxWidth={35}
              percentage={handleComplianceValue(
                standardCompliance.nonComplianceLevel
              )}
              progressColor={getProgressBarColor(
                handleComplianceValue(standardCompliance.nonComplianceLevel)
              )}
            />
          </Text>
        </Col>
      </Row>
      <Row>
        <Col lg={50} md={50} sm={50}>
          <Text ta={"start"}>
            {t(
              "organization.tabs.compliance.tabs.overview.benchmark.bestOrganization"
            )}
          </Text>
        </Col>
        <Col lg={50} md={50} sm={50}>
          <Text ta={"end"}>
            {`${handleComplianceValue(
              standardCompliance.bestOrganizationNonComplianceLevel
            )}%`}{" "}
            <ProgressBar
              height={10}
              maxWidth={35}
              percentage={handleComplianceValue(
                standardCompliance.bestOrganizationNonComplianceLevel
              )}
              progressColor={getProgressBarColor(
                handleComplianceValue(
                  standardCompliance.bestOrganizationNonComplianceLevel
                )
              )}
            />
          </Text>
        </Col>
      </Row>
      <Row>
        <Col lg={50} md={50} sm={50}>
          <Text ta={"start"}>
            {t(
              "organization.tabs.compliance.tabs.overview.benchmark.avgOrganization"
            )}
          </Text>
        </Col>
        <Col lg={50} md={50} sm={50}>
          <Text ta={"end"}>
            {`${handleComplianceValue(
              standardCompliance.avgOrganizationNonComplianceLevel
            )}%`}{" "}
            <ProgressBar
              height={10}
              maxWidth={35}
              percentage={handleComplianceValue(
                standardCompliance.avgOrganizationNonComplianceLevel
              )}
              progressColor={getProgressBarColor(
                handleComplianceValue(
                  standardCompliance.avgOrganizationNonComplianceLevel
                )
              )}
            />
          </Text>
        </Col>
      </Row>
      <Row>
        <Col lg={50} md={50} sm={50}>
          <Text ta={"start"}>
            {t(
              "organization.tabs.compliance.tabs.overview.benchmark.worstOrganization"
            )}
          </Text>
        </Col>
        <Col lg={50} md={50} sm={50}>
          <Text ta={"end"}>
            {`${handleComplianceValue(
              standardCompliance.worstOrganizationNonComplianceLevel
            )}%`}{" "}
            <ProgressBar
              height={10}
              maxWidth={35}
              percentage={handleComplianceValue(
                standardCompliance.worstOrganizationNonComplianceLevel
              )}
              progressColor={getProgressBarColor(
                handleComplianceValue(
                  standardCompliance.worstOrganizationNonComplianceLevel
                )
              )}
            />
          </Text>
        </Col>
      </Row>
    </Card>
  );
};
export { BenchmarkCard };
