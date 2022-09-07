/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";
import { RiCloseFill } from "react-icons/ri";

import {
  NavbarContactButton,
  NavbarList,
} from "../../../../styles/styledComponents";
import { AirsLink } from "../../../AirsLink";
import { Search } from "../../../Search";
import {
  CloseMenuButton,
  CloseMenuButtonContainer,
  DesktopTopbarItem,
  DesktopTopbarItemsContainer,
  TopBarButton,
} from "../../styles/styledComponents";

interface IProps {
  close: () => void;
}

const searchIndices = [
  {
    description: `fluidattacks_airs`,
    keywords: `fluidattacks_airs`,
    name: `fluidattacks_airs`,
    title: `fluidattacks_airs`,
  },
];

const MenuDesktopTopBar: React.FC<IProps> = ({
  close,
}: IProps): JSX.Element => (
  <NavbarList>
    <CloseMenuButtonContainer>
      <CloseMenuButton onClick={close}>
        <RiCloseFill className={"f2 nt1 nl2 c-fluid-bk"} />
      </CloseMenuButton>
      <Search indices={searchIndices} />
    </CloseMenuButtonContainer>
    <DesktopTopbarItemsContainer>
      <DesktopTopbarItem>
        <AirsLink href={"https://app.fluidattacks.com/"}>
          <TopBarButton>{"Log in"}</TopBarButton>
        </AirsLink>
      </DesktopTopbarItem>
      <DesktopTopbarItem className={"dn-m"}>
        <Link className={"no-underline"} to={"/contact-us/"}>
          <TopBarButton onClick={close}>{"Get a Demo"}</TopBarButton>
        </Link>
      </DesktopTopbarItem>
      <DesktopTopbarItem className={"dn-m"}>
        <AirsLink href={"https://try.fluidattacks.com/us/ebook/"}>
          <TopBarButton>{"Download eBook"}</TopBarButton>
        </AirsLink>
      </DesktopTopbarItem>
      <DesktopTopbarItem className={"dib-m dn"}>
        <Link className={"no-underline"} to={"/contact-us/"}>
          <NavbarContactButton onClick={close}>
            {"Contact now"}
          </NavbarContactButton>
        </Link>
      </DesktopTopbarItem>
    </DesktopTopbarItemsContainer>
  </NavbarList>
);

export { MenuDesktopTopBar };
