import React from "react";
import { Route, Switch, useRouteMatch } from "react-router-dom";

import { groupContext } from "../GroupContent/context";
import { ToeContent } from "../ToeContent";
import { Can } from "utils/authz/Can";

const GroupInternalContent: React.FC = (): JSX.Element => {
  const { path, url } = useRouteMatch<{ path: string; url: string }>();

  return (
    <React.StrictMode>
      <groupContext.Provider value={{ url }}>
        <Switch>
          <Can do={"see_internal_toe"}>
            <Route path={`${path}/surface`}>
              <ToeContent isInternal={true} />
            </Route>
          </Can>
        </Switch>
      </groupContext.Provider>
    </React.StrictMode>
  );
};

export { GroupInternalContent };
