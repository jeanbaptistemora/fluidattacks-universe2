/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint import/no-unresolved:0 */
import { faAngleDown } from "@fortawesome/pro-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback, useState } from "react";

import {
  FontAwesomeContainerSmall,
  InnerContentList,
  InnerListContainer,
  InnerListItem,
  ListItem,
  ListItemLabel,
} from "../../../../../styles/styledComponents";
import { BodyLink } from "../BodyLink";

const SystemsList: React.FC = (): JSX.Element => {
  const [isTouch, setIsTouch] = useState(false);
  const handleOpenClose = useCallback((): void => {
    setIsTouch(!isTouch);
  }, [isTouch]);

  return (
    <div>
      <ListItem>
        <ListItemLabel onClick={handleOpenClose}>
          {"Systems"}
          <FontAwesomeContainerSmall>
            <FontAwesomeIcon className={"c-gray-176"} icon={faAngleDown} />
          </FontAwesomeContainerSmall>
        </ListItemLabel>
        <InnerListContainer
          style={{
            animation: "fadein 0.5s",
            display: isTouch ? "block" : "none",
          }}
        >
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
              <BodyLink
                link={"/systems/thick-clients/"}
                name={"Thick Clients"}
              />
            </InnerListItem>
            <InnerListItem>
              <BodyLink
                link={"/systems/apis/"}
                name={"APIs and Microservices"}
              />
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
};

export { SystemsList };
