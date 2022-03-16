/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint import/no-unresolved:0 */
import React, { useCallback, useState } from "react";

import {
  InnerContentList,
  InnerListContainer,
  InnerListItem,
  ListItem,
  ListItemLabel,
} from "../../../../../styles/styledComponents";
import { RotatingArrow } from "../../../../RotatingArrow";
import { BodyLink } from "../BodyLink";

const SolutionsList: React.FC = (): JSX.Element => {
  const [isTouch, setIsTouch] = useState(false);
  const handleOpenClose = useCallback((): void => {
    setIsTouch(!isTouch);
  }, [isTouch]);

  return (
    <div>
      <ListItem>
        <ListItemLabel onClick={handleOpenClose}>
          {"Solutions"}
          <RotatingArrow isTouch={isTouch} />
        </ListItemLabel>
        <InnerListContainer
          style={{
            animation: "fadein 0.5s",
            display: isTouch ? "block" : "none",
          }}
        >
          <InnerContentList>
            <InnerListItem>
              <BodyLink link={"/solutions/devsecops/"} name={"DevSecOps"} />
            </InnerListItem>
            <InnerListItem>
              <BodyLink
                link={"/solutions/secure-code-review/"}
                name={"Secure Code Review"}
              />
            </InnerListItem>
            <InnerListItem>
              <BodyLink link={"/solutions/red-teaming/"} name={"Red Teaming"} />
            </InnerListItem>
            <InnerListItem>
              <BodyLink
                link={"/solutions/attack-simulation/"}
                name={"Breach and Attack Simulation"}
              />
            </InnerListItem>
            <InnerListItem>
              <BodyLink
                link={"/solutions/security-testing/"}
                name={"Security Testing"}
              />
            </InnerListItem>
            <InnerListItem>
              <BodyLink
                link={"/solutions/penetration-testing/"}
                name={"Penetration Testing"}
              />
            </InnerListItem>
            <InnerListItem>
              <BodyLink
                link={"/solutions/ethical-hacking/"}
                name={"Ethical Hacking"}
              />
            </InnerListItem>
            <InnerListItem>
              <BodyLink
                link={"/solutions/vulnerability-management/"}
                name={"Vulnerability Management"}
              />
            </InnerListItem>
          </InnerContentList>
        </InnerListContainer>
      </ListItem>
    </div>
  );
};

export { SolutionsList };
