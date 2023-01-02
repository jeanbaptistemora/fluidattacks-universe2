import React from "react";
import { useTranslation } from "react-i18next";

import { OverviewCard } from "./Card";

import { InfoDropdown } from "components/InfoDropdown";
import { Col } from "components/Layout/Col";
import { Row } from "components/Layout/Row";
import { Text } from "components/Text";
import { Can } from "utils/authz/Can";

interface IOrganizationOverviewProps {
  costsTotal: number;
  numberAuthorsMachine: number;
  numberAuthorsSquad: number;
  numberGroupsMachine: number;
  numberGroupsSquad: number;
  organizationName: string;
}

export const OrganizationOverview: React.FC<IOrganizationOverviewProps> = ({
  costsTotal,
  numberAuthorsMachine,
  numberAuthorsSquad,
  numberGroupsMachine,
  numberGroupsSquad,
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
          <Col>
            <OverviewCard
              content={t(
                "organization.tabs.billing.overview.numberGroupsMachine.content",
                { numberGroupsMachine }
              )}
              info={t(
                "organization.tabs.billing.overview.numberGroupsMachine.info"
              )}
              title={t(
                "organization.tabs.billing.overview.numberGroupsMachine.title"
              )}
            />
          </Col>
          <Col>
            <OverviewCard
              content={t(
                "organization.tabs.billing.overview.numberGroupsSquad.content",
                { numberGroupsSquad }
              )}
              info={t(
                "organization.tabs.billing.overview.numberGroupsSquad.info"
              )}
              title={t(
                "organization.tabs.billing.overview.numberGroupsSquad.title"
              )}
            />
          </Col>
          <Col>
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
          <Col>
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
          <Can do={"api_resolvers_billing_prices_resolve"}>
            <Col>
              <OverviewCard
                content={t(
                  "organization.tabs.billing.overview.costsTotal.content",
                  { costsTotal }
                )}
                info={t("organization.tabs.billing.overview.costsTotal.info")}
                title={t("organization.tabs.billing.overview.costsTotal.title")}
              />
            </Col>
          </Can>
        </Row>
      </Row>
    </React.StrictMode>
  );
};
