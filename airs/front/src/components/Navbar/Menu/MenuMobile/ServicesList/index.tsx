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
