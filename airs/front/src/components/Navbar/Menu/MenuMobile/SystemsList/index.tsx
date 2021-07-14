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

const SystemsList: React.FC = (): JSX.Element => (
  <div>
    <ListItem>
      <ListItemCheckbox
        className={"systems-title"}
        id={"systems-title"}
        name={"systems"}
      />
      <ListItemLabel htmlFor={"systems-title"}>
        {"Systems"}
        <FontAwesomeContainerSmall>
          <FontAwesomeIcon className={"c-gray-176"} icon={faAngleDown} />
        </FontAwesomeContainerSmall>
      </ListItemLabel>
      <InnerListContainer className={"systems-list"}>
        <InnerContentList>
          <InnerListItem>
            <BodyLink link={"/systems/web-apps/"} name={"Web Applications"} />
          </InnerListItem>
          <InnerListItem>
            <BodyLink
              link={"/systems/mobile-apps/"}
              name={"Mobile Applications"}
            />
          </InnerListItem>
          <InnerListItem>
            <BodyLink link={"/systems/thick-clients/"} name={"Thick Clients"} />
          </InnerListItem>
          <InnerListItem>
            <BodyLink link={"/systems/apis/"} name={"APIs and Microservices"} />
          </InnerListItem>
          <InnerListItem>
            <BodyLink
              link={"/systems/cloud-infrastructure/"}
              name={"Cloud Infrastructure"}
            />
          </InnerListItem>
          <InnerListItem>
            <BodyLink
              link={"/systems/networks-and-hosts/"}
              name={"Networks and Hosts"}
            />
          </InnerListItem>
          <InnerListItem>
            <BodyLink link={"/systems/iot/"} name={"Internet of Things"} />
          </InnerListItem>
          <InnerListItem>
            <BodyLink link={"/systems/ot/"} name={"SCADA and OT"} />
          </InnerListItem>
        </InnerContentList>
      </InnerListContainer>
    </ListItem>
  </div>
);

export { SystemsList };
