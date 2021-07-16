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

const ServicesList: React.FC = (): JSX.Element => {
  const [isTouch, setIsTouch] = useState(false);
  const handleOpenClose = useCallback((): void => {
    setIsTouch(!isTouch);
  }, [isTouch]);

  return (
    <div>
      <ListItem>
        <ListItemLabel onClick={handleOpenClose}>
          {"Services"}
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
};

export { ServicesList };
