/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint import/no-unresolved:0 */
import { faTimes } from "@fortawesome/pro-light-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link } from "gatsby";
import React from "react";

import { AboutUsList } from "./AboutUsList";
import { CategoriesList } from "./CategoriesList";
import { LinksSection } from "./LinksSection";
import { ResourcesList } from "./ResourcesList";
import { ServicesList } from "./ServicesList";
import { SolutionsList } from "./SolutionsList";
import { SystemsList } from "./SystemsList";

import {
  ContentContainer,
  ContentList,
  FooterContainer,
  HeaderContainer,
  LogoContainer,
  NavbarContactButton,
  SidebarContainer,
} from "../../../../styles/styledComponents";
import { SocialMedia } from "../../../SocialMedia";
import { DesktopTopbarItem, TopBarButton } from "../../styles/styledComponents";

interface IProps {
  close: () => void;
}

const MenuMobile: React.FC<IProps> = ({ close }: IProps): JSX.Element => (
  <SidebarContainer>
    <HeaderContainer>
      <LogoContainer>
        <FontAwesomeIcon
          className={"f2 nl2 pointer c-fluid-bk"}
          icon={faTimes}
          onClick={close}
        />
      </LogoContainer>
      <div className={"w-50 flex justify-end"}>
        <DesktopTopbarItem>
          <Link className={"no-underline"} to={"https://app.fluidattacks.com/"}>
            <TopBarButton>{"Log in"}</TopBarButton>
          </Link>
        </DesktopTopbarItem>
      </div>
    </HeaderContainer>
    <ContentContainer>
      <ContentList>
        <ServicesList />
        <SolutionsList />
        <SystemsList />
        <div>
          <NavbarContactButton
            className={"mb3 w-90 pv3 justify-center flex center mh3"}
            onClick={close}
          >
            <Link className={"no-underline white f4"} to={"/contact-us/"}>
              {"Contact Now"}
            </Link>
          </NavbarContactButton>
        </div>
        <AboutUsList />
        <CategoriesList />
        <ResourcesList />
      </ContentList>
      <LinksSection />
    </ContentContainer>
    <FooterContainer>
      <p className={"c-fluid-gray"}>{"FOLLOW US"}</p>
      <SocialMedia />
    </FooterContainer>
  </SidebarContainer>
);

export { MenuMobile };
