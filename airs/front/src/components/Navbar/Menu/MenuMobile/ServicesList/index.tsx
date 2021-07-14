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

const ServicesList: React.FC = (): JSX.Element => (
  <div>
    <ListItem>
      <ListItemCheckbox
        className={"services-title"}
        id={"services-title"}
        name={"services"}
      />
      <ListItemLabel htmlFor={"services-title"}>
        {"Services"}
        <FontAwesomeContainerSmall>
          <FontAwesomeIcon className={"c-gray-176"} icon={faAngleDown} />
        </FontAwesomeContainerSmall>
      </ListItemLabel>
      <InnerListContainer className={"services-list"}>
        <InnerContentList>
          <InnerListItem>
            <BodyLink
              link={"/services/continuous-hacking/"}
              name={"Continuous Hacking"}
            />
          </InnerListItem>
          <InnerListItem>
            <BodyLink
              link={"/services/one-shot-hacking/"}
              name={"One-Shot Hacking"}
            />
          </InnerListItem>
          <InnerListItem>
            <BodyLink link={"/services/comparative/"} name={"Comparative"} />
          </InnerListItem>
        </InnerContentList>
      </InnerListContainer>
    </ListItem>
  </div>
);

export { ServicesList };
