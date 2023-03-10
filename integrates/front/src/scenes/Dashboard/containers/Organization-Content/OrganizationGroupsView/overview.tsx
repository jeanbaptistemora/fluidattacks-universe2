import React from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import { InfoDropdown } from "components/InfoDropdown";
import { Col } from "components/Layout/Col";
import { Row } from "components/Layout/Row";
import { Text } from "components/Text";
import { OverviewCard } from "scenes/Dashboard/containers/Organization-Content/OrganizationBillingView/Overview/Card";

interface IOrganizationGroupOverviewProps {
  coveredAuthors: number;
  coveredRepositories: number;
  missedAuthors: number;
  missedRepositories: number;
  organizationName: string;
}

const OrganizationGroupOverview: React.FC<IOrganizationGroupOverviewProps> = ({
  coveredAuthors,
  coveredRepositories,
  missedAuthors,
  missedRepositories,
  organizationName,
}): JSX.Element => {
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
            <Link to={`/orgs/${organizationName}/outside`}>
              <OverviewCard
                content={t(
                  "organization.tabs.groups.overview.coveredAuthors.content",
                  { coveredAuthors }
                )}
                info={t(
                  "organization.tabs.groups.overview.coveredAuthors.info"
                )}
                title={t(
                  "organization.tabs.groups.overview.coveredAuthors.title"
                )}
              />
            </Link>
          </Col>
          <Col lg={25} md={50} sm={100}>
            <Link to={`/orgs/${organizationName}/outside`}>
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
            </Link>
          </Col>
          <Col lg={25} md={50} sm={100}>
            <Link to={`/orgs/${organizationName}/outside`}>
              <OverviewCard
                content={t(
                  "organization.tabs.groups.overview.missedAuthors.content",
                  { missedAuthors }
                )}
                info={t("organization.tabs.groups.overview.missedAuthors.info")}
                title={t(
                  "organization.tabs.groups.overview.missedAuthors.title"
                )}
              />
            </Link>
          </Col>
          <Col lg={25} md={50} sm={100}>
            <Link to={`/orgs/${organizationName}/outside`}>
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
            </Link>
          </Col>
        </Row>
      </Row>
    </React.StrictMode>
  );
};

export { OrganizationGroupOverview };
