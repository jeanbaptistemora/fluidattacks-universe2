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
              <BodyLink link={"/clients/"} name={"Clients"} />
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
