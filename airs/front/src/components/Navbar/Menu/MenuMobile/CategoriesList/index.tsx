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

const CategoriesList: React.FC = (): JSX.Element => {
  const [isTouch, setIsTouch] = useState(false);
  const handleOpenClose = useCallback((): void => {
    setIsTouch(!isTouch);
  }, [isTouch]);

  return (
    <div>
      <ListItem>
        <ListItemLabel onClick={handleOpenClose}>
          {"Categories"}
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
              <BodyLink link={"/product/sast/"} name={"SAST"} />
            </InnerListItem>
            <InnerListItem>
              <BodyLink link={"/product/dast/"} name={"DAST"} />
            </InnerListItem>
            <InnerListItem>
              <BodyLink link={"/solutions/penetration-testing/"} name={"MPT"} />
            </InnerListItem>
            <InnerListItem>
              <BodyLink link={"/product/sca/"} name={"SCA"} />
            </InnerListItem>
            <InnerListItem>
              <BodyLink link={"/product/re/"} name={"RE"} />
            </InnerListItem>
            <InnerListItem>
              <BodyLink link={"/product/ptaas/"} name={"PTaaS"} />
            </InnerListItem>
            <InnerListItem>
              <BodyLink link={"/product/mast/"} name={"MAST"} />
            </InnerListItem>
          </InnerContentList>
        </InnerListContainer>
      </ListItem>
    </div>
  );
};

export { CategoriesList };
