import React from "react";
import { Link } from "react-router-dom";

import { SidebarContainer, SidebarMenu } from "./styles";

import { LoadingAnimation } from "components/LoadingAnimation";
import { Logo } from "components/Logo";
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
            <Logo height={45} width={45} />
          </Link>
        </li>
      </SidebarMenu>
      {isLoading ? <LoadingAnimation /> : undefined}
    </SidebarContainer>
  );
};

export { Sidebar };
