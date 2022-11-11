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
  costsAuthors: number;
  costsBase: number;
  costsTotal: number;
  numberAuthorsMachine: number;
  numberAuthorsSquad: number;
  numberAuthorsTotal: number;
  organizationName: string;
}

export const OrganizationOverview: React.FC<IOrganizationOverviewProps> = ({
  costsAuthors,
  costsBase,
  costsTotal,
  numberAuthorsMachine,
  numberAuthorsSquad,
  numberAuthorsTotal,
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
          <Col lg={33} md={50} sm={100}>
            <OverviewCard
              content={t(
                "organization.tabs.billing.overview.costsBase.content",
                { costsBase }
              )}
              info={t("organization.tabs.billing.overview.costsBase.info")}
              title={t("organization.tabs.billing.overview.costsBase.title")}
            />
          </Col>
          <Col lg={33} md={50} sm={100}>
            <OverviewCard
              content={t(
                "organization.tabs.billing.overview.costsAuthors.content",
                { costsAuthors }
              )}
              info={t("organization.tabs.billing.overview.costsAuthors.info")}
              title={t("organization.tabs.billing.overview.costsAuthors.title")}
            />
          </Col>
          <Col lg={33} md={50} sm={100}>
            <OverviewCard
              content={t(
                "organization.tabs.billing.overview.costsTotal.content",
                { costsTotal }
              )}
              info={t("organization.tabs.billing.overview.costsTotal.info")}
              title={t("organization.tabs.billing.overview.costsTotal.title")}
            />
          </Col>
        </Row>
        <Row>
          <Col lg={33} md={50} sm={100}>
            <OverviewCard
              content={t(
                "organization.tabs.billing.overview.numberAuthorsMachine.content",
                { numberAuthorsMachine }
              )}
              info={t(
                "organization.tabs.billing.overview.numberAuthorsMachine.info"
              )}
              title={t(
                "organization.tabs.billing.overview.numberAuthorsMachine.title"
              )}
            />
          </Col>
          <Col lg={33} md={50} sm={100}>
            <OverviewCard
              content={t(
                "organization.tabs.billing.overview.numberAuthorsSquad.content",
                { numberAuthorsSquad }
              )}
              info={t(
                "organization.tabs.billing.overview.numberAuthorsSquad.info"
              )}
              title={t(
                "organization.tabs.billing.overview.numberAuthorsSquad.title"
              )}
            />
          </Col>
          <Col lg={33} md={50} sm={100}>
            <OverviewCard
              content={t(
                "organization.tabs.billing.overview.numberAuthorsTotal.content",
                { numberAuthorsTotal }
              )}
              info={t(
                "organization.tabs.billing.overview.numberAuthorsTotal.info"
              )}
              title={t(
                "organization.tabs.billing.overview.numberAuthorsTotal.title"
              )}
            />
          </Col>
        </Row>
      </Row>
    </React.StrictMode>
  );
};
