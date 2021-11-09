import { track } from "mixpanel-browser";
import React, { useEffect } from "react";
import { useParams } from "react-router-dom";

import { Unsubscribe } from "./Unsubscribe";

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

  // Side effects
  const onMount: () => void = (): void => {
    track("GroupResources");
  };
  useEffect(onMount, []);

  return (
    <React.StrictMode>
      <div id={"resources"}>
        <Files groupName={groupName} />
        <hr />
        <Portfolio groupName={groupName} />
        <Can do={"api_mutations_update_group_mutate"}>
          <React.Fragment>
            <hr />
            <Services groupName={groupName} />
          </React.Fragment>
        </Can>
        <GroupInformation />
        <Can do={"api_resolvers_group_forces_token_resolve"}>
          <Have I={"has_forces"}>
            <AgentToken groupName={groupName} />
          </Have>
        </Can>
        <hr />
        <AccessInfo />
        <Can do={"api_mutations_unsubscribe_from_group_mutate"}>
          <React.Fragment>
            <hr />
            <Unsubscribe />
          </React.Fragment>
        </Can>
        <Can do={"api_mutations_remove_group_mutate"}>
          <React.Fragment>
            <hr />
            <DeleteGroup />
          </React.Fragment>
        </Can>
      </div>
    </React.StrictMode>
  );
};

export { GroupSettingsView };
