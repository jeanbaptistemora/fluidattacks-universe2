import React from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { Unsubscribe } from "./Unsubscribe";

import { Card } from "components/Card";
import { Col, Row } from "components/Layout";
import { AccessInfo } from "scenes/Dashboard/containers/GroupSettingsView/AccessInfo";
import { AgentToken } from "scenes/Dashboard/containers/GroupSettingsView/AgentToken";
import { DeleteGroup } from "scenes/Dashboard/containers/GroupSettingsView/DeleteGroup";
import { Files } from "scenes/Dashboard/containers/GroupSettingsView/Files";
import { GroupInformation } from "scenes/Dashboard/containers/GroupSettingsView/Info";
import { Portfolio } from "scenes/Dashboard/containers/GroupSettingsView/Portfolio";
import { Services } from "scenes/Dashboard/containers/GroupSettingsView/Services";
import { Can } from "utils/authz/Can";
import { Have } from "utils/authz/Have";

const GroupSettingsView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const { t } = useTranslation();

  return (
    <React.StrictMode>
      <Row id={"resources"}>
        <Col large={"100"} medium={"100"} small={"100"}>
          <Files groupName={groupName} />
        </Col>
        <Col large={"100"} medium={"100"} small={"100"}>
          <Portfolio groupName={groupName} />
        </Col>
        <Can do={"api_mutations_update_group_mutate"}>
          <Col large={"100"} medium={"100"} small={"100"}>
            <Services groupName={groupName} />
          </Col>
        </Can>
        <Col large={"100"} medium={"100"} small={"100"}>
          <GroupInformation />
        </Col>
        <Col large={"100"} medium={"100"} small={"100"}>
          <AccessInfo />
        </Col>
        <Can do={"api_resolvers_group_forces_token_resolve"}>
          <Have I={"has_forces"}>
            <Col large={"33"} medium={"50"} small={"100"}>
              <Card title={t("searchFindings.agentTokenSection.title")}>
                <AgentToken groupName={groupName} />
              </Card>
            </Col>
          </Have>
        </Can>
        <Can do={"api_mutations_unsubscribe_from_group_mutate"}>
          <Col large={"34"} medium={"50"} small={"100"}>
            <Card title={t("searchFindings.servicesTable.unsubscribe.title")}>
              <Unsubscribe />
            </Card>
          </Col>
        </Can>
        <Can do={"api_mutations_remove_group_mutate"}>
          <Col large={"33"} medium={"50"} small={"100"}>
            <Card
              title={t("searchFindings.servicesTable.deleteGroup.deleteGroup")}
            >
              <DeleteGroup />
            </Card>
          </Col>
        </Can>
      </Row>
    </React.StrictMode>
  );
};

export { GroupSettingsView };
