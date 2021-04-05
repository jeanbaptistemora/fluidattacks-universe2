import { track } from "mixpanel-browser";
import React, { useEffect } from "react";
import { useParams } from "react-router";

import { Unsubscribe } from "./Unsubscribe";

import { AgentToken } from "scenes/Dashboard/containers/ProjectSettingsView/AgentToken";
import { DeleteGroup } from "scenes/Dashboard/containers/ProjectSettingsView/DeleteGroup";
import { Files } from "scenes/Dashboard/containers/ProjectSettingsView/Files";
import { GroupInformation } from "scenes/Dashboard/containers/ProjectSettingsView/Info";
import { Portfolio } from "scenes/Dashboard/containers/ProjectSettingsView/Portfolio";
import { Services } from "scenes/Dashboard/containers/ProjectSettingsView/Services";
import { Can } from "utils/authz/Can";
import { Have } from "utils/authz/Have";

const ProjectSettingsView: React.FC = (): JSX.Element => {
  const { projectName } = useParams<{ projectName: string }>();

  // Side effects
  const onMount: () => void = (): void => {
    track("ProjectResources");
  };
  useEffect(onMount, []);

  return (
    <React.StrictMode>
      <div id={"resources"}>
        <Files projectName={projectName} />
        <hr />
        <Portfolio projectName={projectName} />
        <Can do={"backend_api_mutations_edit_group_mutate"}>
          <React.Fragment>
            <hr />
            <Services groupName={projectName} />
          </React.Fragment>
        </Can>
        <GroupInformation />
        <Can do={"backend_api_resolvers_group_forces_token_resolve"}>
          <Have I={"has_forces"}>
            <AgentToken groupName={projectName} />
          </Have>
        </Can>
        <Can do={"backend_api_mutations_unsubscribe_from_group_mutate"}>
          <React.Fragment>
            <hr />
            <Unsubscribe />
          </React.Fragment>
        </Can>
        <Can do={"backend_api_mutations_remove_group_mutate"}>
          <React.Fragment>
            <hr />
            <DeleteGroup />
          </React.Fragment>
        </Can>
      </div>
    </React.StrictMode>
  );
};

export { ProjectSettingsView };
