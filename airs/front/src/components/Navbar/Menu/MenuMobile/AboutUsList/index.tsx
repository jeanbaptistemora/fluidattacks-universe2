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

const AboutUsList: React.FC = (): JSX.Element => (
  <div>
    <ListItem>
      <ListItemCheckbox
        className={"aboutus-title"}
        id={"aboutus-title"}
        name={"aboutus"}
      />
      <ListItemLabel htmlFor={"aboutus-title"}>
        {"About Us"}
        <FontAwesomeContainerSmall>
          <FontAwesomeIcon className={"c-gray-176"} icon={faAngleDown} />
        </FontAwesomeContainerSmall>
      </ListItemLabel>
      <InnerListContainer className={"aboutus-list"}>
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

export { AboutUsList };
