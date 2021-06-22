/* eslint react/forbid-component-props: 0 */
import { faTimes } from "@fortawesome/pro-light-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link } from "gatsby";
import React from "react";

import {
  NavbarContactButton,
  NavbarList,
} from "../../../../styles/styledComponents";
import { Search } from "../../../Search";
import {
  CloseMenuButton,
  CloseMenuButtonContainer,
  TopBarButton,
} from "../../styles/navbarStyledComponents";

interface IProps {
  close: () => void;
}

const searchIndices = [
  { name: `fluidattacks_airs`, title: `fluidattacks_airs` },
];

const MenuDesktopTopBar: React.FC<IProps> = ({
  close,
}: IProps): JSX.Element => (
  <NavbarList>
    <CloseMenuButtonContainer>
      <CloseMenuButton onClick={close}>
        <FontAwesomeIcon className={"f2 nt1 nl2 c-fluid-bk"} icon={faTimes} />
      </CloseMenuButton>
      <Search indices={searchIndices} />
    </CloseMenuButtonContainer>
    <li className={"fr pv4 dib-m dn"}>
      <Link className={"no-underline"} to={"/contact-us/"}>
        <NavbarContactButton onClick={close}>
          {"Contact now"}
        </NavbarContactButton>
      </Link>
    </li>
    <li className={"fr mr3 pv4 dn-m"}>
      <Link
        className={"no-underline"}
        to={"https://landing.fluidattacks.com/us/ebook/"}
      >
        <TopBarButton>{"Download eBook"}</TopBarButton>
      </Link>
    </li>
    <li className={"fr mr3 pv4 dn-m"}>
      <Link className={"no-underline"} to={"/contact-us/"}>
        <TopBarButton onClick={close}>{"Get a Demo"}</TopBarButton>
      </Link>
    </li>
    <li className={"fr mr3 pv4"}>
      <Link className={"no-underline"} to={"https://app.fluidattacks.com/"}>
        <TopBarButton>{"Log in"}</TopBarButton>
      </Link>
    </li>
  </NavbarList>
);

export { MenuDesktopTopBar };
