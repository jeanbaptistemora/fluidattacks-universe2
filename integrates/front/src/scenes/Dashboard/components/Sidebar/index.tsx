import React from "react";
import { Link } from "react-router-dom";

import { Logo, Preloader, SidebarContainer, SidebarMenu } from "./styles";

import { useApolloNetworkStatus } from "utils/apollo";

const Sidebar: React.FC = (): JSX.Element => {
  const status = useApolloNetworkStatus();
  const isLoading: boolean =
    status.numPendingQueries > 0 || status.numPendingMutations > 0;

  return (
    <SidebarContainer>
      <SidebarMenu>
        <li>
          <Link to={"/home"}>
            <Logo />
          </Link>
        </li>
      </SidebarMenu>
      {isLoading ? <Preloader /> : undefined}
    </SidebarContainer>
  );
};

export { Sidebar };
