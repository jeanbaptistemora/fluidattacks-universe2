/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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
            <InnerListItem>
              <BodyLink link={"/categories/mast/"} name={"MAST"} />
            </InnerListItem>
          </InnerContentList>
        </InnerListContainer>
      </ListItem>
    </div>
  );
};

export { CategoriesList };
