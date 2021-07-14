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

const CategoriesList: React.FC = (): JSX.Element => (
  <div>
    <ListItem>
      <ListItemCheckbox
        className={"categories-title"}
        id={"categories-title"}
        name={"categories"}
      />
      <ListItemLabel htmlFor={"categories-title"}>
        {"Categories"}
        <FontAwesomeContainerSmall>
          <FontAwesomeIcon className={"c-gray-176"} icon={faAngleDown} />
        </FontAwesomeContainerSmall>
      </ListItemLabel>
      <InnerListContainer className={"categories-list"}>
        <InnerContentList>
          <InnerListItem>
            <BodyLink link={"/categories/sast/"} name={"SAST"} />
          </InnerListItem>
          <InnerListItem>
            <BodyLink link={"/categories/dast/"} name={"DAST"} />
          </InnerListItem>
          <InnerListItem>
            <BodyLink link={"/solutions/penetration-testing/"} name={"MPT"} />
          </InnerListItem>
          <InnerListItem>
            <BodyLink link={"/categories/sca/"} name={"SCA"} />
          </InnerListItem>
          <InnerListItem>
            <BodyLink link={"/categories/re/"} name={"RE"} />
          </InnerListItem>
          <InnerListItem>
            <BodyLink link={"/categories/ptaas/"} name={"PTaaS"} />
          </InnerListItem>
        </InnerContentList>
      </InnerListContainer>
    </ListItem>
  </div>
);

export { CategoriesList };
