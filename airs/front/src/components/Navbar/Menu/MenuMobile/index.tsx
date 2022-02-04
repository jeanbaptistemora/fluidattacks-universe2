/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint import/no-unresolved:0 */
import { Link } from "gatsby";
import React from "react";
import { RiCloseFill } from "react-icons/ri";

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
  HeaderContainer,
  LogoContainer,
  MobileContactButton,
  MobileFooterContainer,
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
        <RiCloseFill className={"f2 nl2 pointer c-fluid-bk"} onClick={close} />
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
        <div className={"mv4"}>
          <Link className={"no-underline"} to={"/contact-us/"}>
            <MobileContactButton onClick={close}>
              {"Contact Now"}
            </MobileContactButton>
          </Link>
        </div>
        <AboutUsList />
        <CategoriesList />
        <ResourcesList />
      </ContentList>
      <LinksSection />
    </ContentContainer>
    <MobileFooterContainer>
      <p className={"c-fluid-gray"}>{"FOLLOW US"}</p>
      <SocialMedia />
    </MobileFooterContainer>
  </SidebarContainer>
);

export { MenuMobile };
