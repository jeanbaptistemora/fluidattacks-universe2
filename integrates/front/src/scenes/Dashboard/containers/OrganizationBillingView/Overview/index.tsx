/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";
import { useTranslation } from "react-i18next";

import { OverviewCard } from "./Card";

import { InfoDropdown } from "components/InfoDropdown";
import { Col } from "components/Layout/Col";
import { Row } from "components/Layout/Row";
import { Text } from "components/Text";

interface IOrganizationOverviewProps {
  currentAuthors: number;
  currentSpend: number;
  organizationName: string;
}

export const OrganizationOverview: React.FC<IOrganizationOverviewProps> = ({
  currentAuthors,
  currentSpend,
  organizationName,
}: IOrganizationOverviewProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <React.StrictMode>
      <Row>
        <Text fw={7} mb={3} mt={2} size={"big"}>
          {t("organization.tabs.billing.overview.title.text")}{" "}
          <InfoDropdown>
            <Text size={"small"} ta={"center"}>
              {t("organization.tabs.billing.overview.title.info", {
                organizationName,
              })}
            </Text>
          </InfoDropdown>
        </Text>
        <Row>
          <Col lg={50} md={50} sm={50}>
            <OverviewCard
              content={t(
                "organization.tabs.billing.overview.currentAuthors.content",
                { currentAuthors }
              )}
              info={t("organization.tabs.billing.overview.currentAuthors.info")}
              title={t(
                "organization.tabs.billing.overview.currentAuthors.title"
              )}
            />
          </Col>
          <Col lg={50} md={50} sm={50}>
            <OverviewCard
              content={t(
                "organization.tabs.billing.overview.currentSpend.content",
                { currentSpend }
              )}
              info={t("organization.tabs.billing.overview.currentSpend.info")}
              title={t("organization.tabs.billing.overview.currentSpend.title")}
            />
          </Col>
        </Row>
      </Row>
    </React.StrictMode>
  );
};
