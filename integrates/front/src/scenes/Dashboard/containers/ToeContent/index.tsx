/* eslint-disable react-hooks/rules-of-hooks */
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import React, { useContext } from "react";
import { useTranslation } from "react-i18next";
import { Redirect, Route, Switch, useRouteMatch } from "react-router-dom";

import type { IToeContentProps } from "./types";

import { groupContext } from "../GroupContent/context";
import type { IGroupContext } from "../GroupContent/types";
import { GroupToeInputsView } from "../GroupToeInputsView";
import { GroupToeLinesView } from "../GroupToeLinesView";
import { Tab, Tabs } from "components/Tabs";
import { TabContent } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";

const toeContent: React.FC<IToeContentProps> = ({
  isInternal,
}: IToeContentProps): JSX.Element => {
  const { t } = useTranslation();
  const { path, url } = useRouteMatch<{ path: string; url: string }>();
  const { path: groupPath }: IGroupContext = useContext(groupContext);

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canGetToeLines: boolean = permissions.can(
    "api_resolvers_group_toe_lines_resolve"
  );
  const canGetToeInputs: boolean = permissions.can(
    "api_resolvers_group_toe_inputs_resolve"
  );

  return (
    <React.StrictMode>
      <div>
        <Tabs>
          <Can do={"api_resolvers_group_toe_lines_resolve"}>
            <Tab
              id={"toeLinesTab"}
              link={`${url}/lines`}
              tooltip={t("group.toe.tabs.lines.tooltip")}
            >
              {t("group.toe.tabs.lines.text")}
            </Tab>
          </Can>
          <Can do={"api_resolvers_group_toe_inputs_resolve"}>
            <Tab
              id={"toeInputsTab"}
              link={`${url}/inputs`}
              tooltip={t("group.toe.tabs.inputs.tooltip")}
            >
              {t("group.toe.tabs.inputs.text")}
            </Tab>
          </Can>
        </Tabs>
      </div>
      <TabContent>
        <Switch>
          <Route exact={true} path={`${path}/lines`}>
            <GroupToeLinesView isInternal={isInternal} />
          </Route>
          <Route exact={true} path={`${path}/inputs`}>
            <GroupToeInputsView isInternal={isInternal} />
          </Route>
          {canGetToeLines ? <Redirect to={`${path}/lines`} /> : undefined}
          {canGetToeInputs ? <Redirect to={`${path}/inputs`} /> : undefined}
          <Redirect to={groupPath} />
        </Switch>
      </TabContent>
    </React.StrictMode>
  );
};

export { toeContent as ToeContent };
