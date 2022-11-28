import React from "react";
import { useTranslation } from "react-i18next";

import { InfoDropdown } from "components/InfoDropdown";
import { Col } from "components/Layout/Col";
import { Row } from "components/Layout/Row";
import { Text } from "components/Text";
import { OverviewCard } from "scenes/Dashboard/containers/OrganizationBillingView/Overview/Card";

interface IOrganizationGroupOverviewProps {
  coveredCommits: number;
  coveredRepositories: number;
  missedCommits: number;
  missedRepositories: number;
  organizationName: string;
}

const OrganizationGroupOverview: React.FC<IOrganizationGroupOverviewProps> = ({
  coveredCommits,
  coveredRepositories,
  missedCommits,
  missedRepositories,
  organizationName,
}: IOrganizationGroupOverviewProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <React.StrictMode>
      <Row>
        <Text fw={7} mb={3} mt={2} size={"big"}>
          {t("organization.tabs.groups.overview.title.text")}{" "}
          <InfoDropdown>
            <Text size={"small"} ta={"center"}>
              {t("organization.tabs.groups.overview.title.info", {
                organizationName,
              })}
            </Text>
          </InfoDropdown>
        </Text>
        <Row>
          <Col lg={25} md={50} sm={100}>
            <OverviewCard
              content={t(
                "organization.tabs.groups.overview.coveredCommits.content",
                { coveredCommits }
              )}
              info={t("organization.tabs.groups.overview.coveredCommits.info")}
              title={t(
                "organization.tabs.groups.overview.coveredCommits.title"
              )}
            />
          </Col>
          <Col lg={25} md={50} sm={100}>
            <OverviewCard
              content={t(
                "organization.tabs.groups.overview.coveredRepositories.content",
                { coveredRepositories }
              )}
              info={t(
                "organization.tabs.groups.overview.coveredRepositories.info"
              )}
              title={t(
                "organization.tabs.groups.overview.coveredRepositories.title"
              )}
            />
          </Col>
          <Col lg={25} md={50} sm={100}>
            <OverviewCard
              content={t(
                "organization.tabs.groups.overview.missedCommits.content",
                { missedCommits }
              )}
              info={t("organization.tabs.groups.overview.missedCommits.info")}
              title={t("organization.tabs.groups.overview.missedCommits.title")}
            />
          </Col>
          <Col lg={25} md={50} sm={100}>
            <OverviewCard
              content={t(
                "organization.tabs.groups.overview.missedRepositories.content",
                { missedRepositories }
              )}
              info={t(
                "organization.tabs.groups.overview.missedRepositories.info"
              )}
              title={t(
                "organization.tabs.groups.overview.missedRepositories.title"
              )}
            />
          </Col>
        </Row>
      </Row>
    </React.StrictMode>
  );
};

export { OrganizationGroupOverview };
