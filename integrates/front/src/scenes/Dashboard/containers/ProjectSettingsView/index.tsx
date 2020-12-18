/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that defines the headers of the table
 */
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { useParams } from "react-router";

import { DeleteGroup } from "scenes/Dashboard/containers/ProjectSettingsView/DeleteGroup";
import { Files } from "scenes/Dashboard/containers/ProjectSettingsView/Files";
import { Portfolio } from "scenes/Dashboard/containers/ProjectSettingsView/Portfolio";
import { Services } from "scenes/Dashboard/containers/ProjectSettingsView/Services";
import { Can } from "utils/authz/Can";

const projectSettingsView: React.FC = (): JSX.Element => {
  const { projectName } = useParams<{ projectName: string }>();
  const { userName } = window as typeof window & Dictionary<string>;

  // Side effects
  const onMount: () => void = (): void => {
    mixpanel.track("ProjectResources", { User: userName });
  };
  React.useEffect(onMount, []);

  return (
    <React.StrictMode>
      <div id="resources">
        <Files projectName={projectName} />
        <hr />
        <Portfolio projectName={projectName} />
        <Can do="backend_api_resolvers_project__do_edit_group">
          <React.Fragment>
            <hr />
            <Services groupName={projectName} />
          </React.Fragment>
        </Can>
        <Can do="backend_api_mutations_remove_group_mutate">
          <React.Fragment>
            <hr />
            <DeleteGroup />
          </React.Fragment>
        </Can>
      </div>
    </React.StrictMode>
  );
};

export { projectSettingsView as ProjectSettingsView };
