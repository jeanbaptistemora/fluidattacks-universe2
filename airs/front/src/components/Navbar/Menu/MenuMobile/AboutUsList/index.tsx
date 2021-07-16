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

const AboutUsList: React.FC = (): JSX.Element => {
  const [isTouch, setIsTouch] = useState(false);
  const handleOpenClose = useCallback((): void => {
    setIsTouch(!isTouch);
  }, [isTouch]);

  return (
    <div>
      <ListItem>
        <ListItemLabel onClick={handleOpenClose}>
          {"About Us"}
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
              <BodyLink link={"/about-us/clients/"} name={"Clients"} />
            </InnerListItem>
            <InnerListItem>
              <BodyLink
                link={"/about-us/certifications/"}
                name={"Certifications"}
              />
            </InnerListItem>
            <InnerListItem>
              <BodyLink
                link={"/about-us/differentiators/"}
                name={"Differentiators"}
              />
            </InnerListItem>
            <InnerListItem>
              <BodyLink link={"/about-us/values/"} name={"Values"} />
            </InnerListItem>
            <InnerListItem>
              <BodyLink link={"/about-us/reviews/"} name={"Reviews"} />
            </InnerListItem>
            <InnerListItem>
              <BodyLink link={"/about-us/events/"} name={"Events"} />
            </InnerListItem>
            <InnerListItem>
              <BodyLink link={"/about-us/people/"} name={"People"} />
            </InnerListItem>
            <InnerListItem>
              <BodyLink
                link={"https://docs.fluidattacks.com/about/security/"}
                name={"Security"}
              />
            </InnerListItem>
          </InnerContentList>
        </InnerListContainer>
      </ListItem>
    </div>
  );
};

export { AboutUsList };
