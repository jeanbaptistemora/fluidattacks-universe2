/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React, { useLayoutEffect, useState } from "react";

import { NavbarItems } from "./NavbarItems";

import {
  NavbarContainer,
  NavbarInnerContainer,
} from "../../styles/styledComponents";

export const NavbarComponent: React.FC = (): JSX.Element => {
  const [scrollTop, setScrollTop] = useState(false);

  const onScroll = (): void => {
    const scrolled = window.scrollY;
    if (scrolled > 5) {
      setScrollTop(true);
    } else {
      setScrollTop(false);
    }
  };

  useLayoutEffect((): (() => void) => {
    window.addEventListener("scroll", onScroll);

    return (): void => {
      window.removeEventListener("scroll", onScroll);
    };
  }, []);

  return (
    <NavbarContainer id={"navbar"} isScrolled={scrollTop}>
      <NavbarInnerContainer id={"inner_navbar"}>
        <NavbarItems />
      </NavbarInnerContainer>
    </NavbarContainer>
  );
};
