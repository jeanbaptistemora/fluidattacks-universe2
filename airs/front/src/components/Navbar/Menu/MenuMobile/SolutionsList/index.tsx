/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint import/no-unresolved:0 */
import { faAngleDown } from "@fortawesome/pro-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

import {
  FontAwesomeContainerSmall,
  InnerContentList,
  InnerListContainer,
  InnerListItem,
  ListItem,
  ListItemCheckbox,
  ListItemLabel,
} from "../../../../../styles/styledComponents";
import { BodyLink } from "../BodyLink";

const SolutionsList: React.FC = (): JSX.Element => (
  <div>
    <ListItem>
      <ListItemCheckbox
        className={"solutions-title"}
        id={"solutions-title"}
        name={"solutions"}
      />
      <ListItemLabel htmlFor={"solutions-title"}>
        {"Solutions"}
        <FontAwesomeContainerSmall>
          <FontAwesomeIcon className={"c-gray-176"} icon={faAngleDown} />
        </FontAwesomeContainerSmall>
      </ListItemLabel>
      <InnerListContainer className={"solutions-list"}>
        <InnerContentList>
          <InnerListItem>
            <BodyLink link={"/solutions/devsecops/"} name={"DevSecOps"} />
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
              link={"/solutions/secure-code-review/"}
              name={"Secure Code Review"}
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

export { SolutionsList };
