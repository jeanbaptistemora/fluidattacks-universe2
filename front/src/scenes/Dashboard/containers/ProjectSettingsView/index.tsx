/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Can } from "../../../../utils/authz/Can";
import { Environments } from "./Environments";
import { Files } from "./Files";
import { Portfolio } from "./Portfolio";
import { Repositories } from "./Repositories";
import { Services } from "./Services";
import { ISettingsViewProps } from "./types";

const projectSettingsView: React.FC<ISettingsViewProps> = (props: ISettingsViewProps): JSX.Element => {
  const { projectName } = props.match.params;
  const { userName } = window as typeof window & Dictionary<string>;

  // Side effects
  const onMount: (() => void) = (): void => {
    mixpanel.track("ProjectResources", { User: userName });
  };
  React.useEffect(onMount, []);

  return (
    <React.StrictMode>
      <div id="resources" className="tab-pane cont active">
        <Repositories projectName={projectName} />
        <hr />
        <Environments projectName={projectName} />
        <hr />
        <Files projectName={projectName} />
        <hr />
        <Portfolio projectName={projectName} />
        <Can do="backend_api_resolvers_project__do_edit_group">
          <React.Fragment>
            <hr />
            <Services groupName={projectName} />
          </React.Fragment>
        </Can>
      </div>
    </React.StrictMode>
  );
};

export { projectSettingsView as ProjectSettingsView };
