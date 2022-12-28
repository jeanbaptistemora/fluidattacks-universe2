import React from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { Unsubscribe } from "./Unsubscribe";

import { Card } from "components/Card";
import { Col, Hr, Row } from "components/Layout";
import { Text } from "components/Text";
import { AccessInfo } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/AccessInfo";
import { AgentToken } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/AgentToken";
import { DeleteGroup } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/DeleteGroup";
import { Files } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/Files";
import { GroupInformation } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/Info";
import { Portfolio } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/Portfolio";
import { Services } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/Services";
import { GroupPolicies } from "scenes/Dashboard/containers/Organization-Content/PoliciesView/Group/index";
import { Can } from "utils/authz/Can";
import { Have } from "utils/authz/Have";

const GroupSettingsView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const { t } = useTranslation();

  return (
    <React.StrictMode>
      <div id={"resources"}>
        <Text fw={7} mb={3} mt={4} size={"big"}>
          {t("searchFindings.tabResources.files.title")}
        </Text>
        <Card>
          <Files groupName={groupName} />
        </Card>
        <Text fw={7} mb={3} mt={4} size={"big"}>
          {t("searchFindings.tabResources.tags.title")}
        </Text>
        <Card>
          <Portfolio groupName={groupName} />
        </Card>
        <Can do={"see_group_services_info"}>
          <Text fw={7} mb={3} mt={4} size={"big"}>
            {t("searchFindings.servicesTable.services")}
          </Text>
          <Services groupName={groupName} />
        </Can>
        <Text fw={7} mb={3} mt={4} size={"big"}>
          {t("searchFindings.infoTable.title")}
        </Text>
        <GroupInformation />
        <GroupPolicies />
        <Hr mv={32} />
        <Row>
          <AccessInfo />
          <Can do={"api_resolvers_group_forces_token_resolve"}>
            <Have I={"has_forces"}>
              <Col lg={33} md={50} sm={100}>
                <Card title={t("searchFindings.agentTokenSection.title")}>
                  <AgentToken groupName={groupName} />
                </Card>
              </Col>
            </Have>
          </Can>
          <Can do={"api_mutations_unsubscribe_from_group_mutate"}>
            <Col lg={34} md={50} sm={100}>
              <Card title={t("searchFindings.servicesTable.unsubscribe.title")}>
                <Unsubscribe />
              </Card>
            </Col>
          </Can>
          <Can do={"api_mutations_remove_group_mutate"}>
            <Col lg={33} md={50} sm={100}>
              <Card
                title={t(
                  "searchFindings.servicesTable.deleteGroup.deleteGroup"
                )}
              >
                <DeleteGroup />
              </Card>
            </Col>
          </Can>
        </Row>
      </div>
    </React.StrictMode>
  );
};

export { GroupSettingsView };
