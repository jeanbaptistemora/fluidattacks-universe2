import type { FC, ReactNode } from "react";
import React from "react";

import type { TVariant } from "./styles";
import { NavBox, NavHeader, NavMenu } from "./styles";

import { ExternalLink } from "components/ExternalLink";
import { Text } from "components/Text";
import { Tooltip } from "components/Tooltip";
import {
  CI_COMMIT_SHA,
  CI_COMMIT_SHORT_SHA,
  INTEGRATES_DEPLOYMENT_DATE,
} from "utils/ctx";

interface INavBarProps {
  children?: ReactNode;
  header?: ReactNode;
  variant?: TVariant;
}

const repo = "https://gitlab.com/fluidattacks/universe/-/tree/";

const NavBar: FC<INavBarProps> = ({
  children,
  header,
  variant = "dark",
}: Readonly<INavBarProps>): JSX.Element => {
  return (
    <NavBox id={"navbar"} variant={variant}>
      <NavHeader>
        {header === undefined ? (
          <div>
            <Text disp={"inline-block"} fw={7} mr={2} tone={"light"}>
              {"Attack Resistance Management"}
            </Text>
            <Tooltip
              disp={"inline-block"}
              id={"app-tooltip"}
              place={"right"}
              tip={INTEGRATES_DEPLOYMENT_DATE}
            >
              <ExternalLink href={`${repo}${CI_COMMIT_SHA}`}>
                <Text
                  bright={8}
                  disp={"inline-block"}
                  size={"small"}
                  tone={"light"}
                >
                  {`v. ${CI_COMMIT_SHORT_SHA}`}
                </Text>
              </ExternalLink>
            </Tooltip>
          </div>
        ) : (
          header
        )}
      </NavHeader>
      <NavMenu>{children}</NavMenu>
    </NavBox>
  );
};

export { NavBar };
