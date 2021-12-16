import React from "react";
import { Route, Switch, useRouteMatch } from "react-router-dom";

import { groupContext } from "../GroupContent/context";
import { ToeContent } from "../ToeContent";

const GroupInternalContent: React.FC = (): JSX.Element => {
  const { path, url } = useRouteMatch<{ path: string; url: string }>();

  return (
    <React.StrictMode>
      <groupContext.Provider value={{ url }}>
        <Switch>
          <Route path={`${path}/surface`}>
            <ToeContent isInternal={true} />
          </Route>
        </Switch>
      </groupContext.Provider>
    </React.StrictMode>
  );
};

export { GroupInternalContent };
