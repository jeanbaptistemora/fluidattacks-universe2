/* eslint-disable react-hooks/rules-of-hooks */
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import React from "react";
import { Redirect, Route, Switch, useRouteMatch } from "react-router-dom";

import { GroupToeInputsView } from "../GroupToeInputsView";
import { GroupToeLinesView } from "../GroupToeLinesView";
import { ContentTab } from "scenes/Dashboard/components/ContentTab";
import {
  StickyContainer,
  TabContent,
  TabsContainer,
} from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { translate } from "utils/translations/translate";

const toeContent: React.FC = (): JSX.Element => {
  const { path, url } = useRouteMatch<{ path: string; url: string }>();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canGetToeLines: boolean = permissions.can(
    "api_resolvers_git_root_services_toe_lines_resolve"
  );
  const canGetToeInputs: boolean = permissions.can(
    "api_resolvers_group_toe_inputs_resolve"
  );

  return (
    <React.StrictMode>
      <StickyContainer>
        <TabsContainer>
          <Can do={"api_resolvers_git_root_services_toe_lines_resolve"}>
            <ContentTab
              icon={"icon pe-7s-menu"}
              id={"toeLinesTab"}
              link={`${url}/lines`}
              title={translate.t("group.toe.tabs.lines.text")}
              tooltip={translate.t("group.toe.tabs.lines.tooltip")}
            />
          </Can>
          <Can do={"api_resolvers_group_toe_inputs_resolve"}>
            <ContentTab
              icon={"icon pe-7s-target"}
              id={"toeInputsTab"}
              link={`${url}/inputs`}
              title={translate.t("group.toe.tabs.inputs.text")}
              tooltip={translate.t("group.toe.tabs.inputs.tooltip")}
            />
          </Can>
        </TabsContainer>
      </StickyContainer>
      <TabContent>
        <Switch>
          <Route
            component={GroupToeLinesView}
            exact={true}
            path={`${path}/lines`}
          />
          <Route
            component={GroupToeInputsView}
            exact={true}
            path={`${path}/inputs`}
          />
          {canGetToeLines ? <Redirect to={`${path}/lines`} /> : undefined}
          {canGetToeInputs ? <Redirect to={`${path}/inputs`} /> : undefined}
        </Switch>
      </TabContent>
    </React.StrictMode>
  );
};

export { toeContent as ToeContent };
