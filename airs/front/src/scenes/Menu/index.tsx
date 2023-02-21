/* eslint react/forbid-component-props: 0 */
import { useMatomo } from "@datapunt/matomo-tracker-react";
import { Link } from "gatsby";
import React, { createRef, useCallback, useState } from "react";
import type { RefObject } from "react";
import { BsFillPersonFill } from "react-icons/bs";
import { FiMenu } from "react-icons/fi";

import { CompanyMenu } from "./Categories/Company";
import { PlatformMenu } from "./Categories/Platform";
import { ResourcesMenu } from "./Categories/Resources";
import { ServiceMenu } from "./Categories/Service";
import { DropdownMenu } from "./MobileMenu/DropdownMenu";
import { useClickOutside } from "./MobileMenu/Search/useClickOutside";
import { NavbarContainer } from "./styles/styledComponents";

import { AirsLink } from "../../components/AirsLink";
import { Button } from "../../components/Button";
import { CloudImage } from "../../components/CloudImage";
import { Container } from "../../components/Container";
import { Text } from "../../components/Typography";
import {
  NavbarInnerContainer,
  NavbarList,
} from "../../styles/styledComponents";
import { useWindowSize } from "../../utils/hooks/useWindowSize";

export const NavbarComponent: React.FC = (): JSX.Element => {
  const { trackEvent } = useMatomo();
  const { width } = useWindowSize();
  const [menuStatus, setMenuStatus] = useState(0);
  const [categoryServices, setCategoryServices] = useState(false);
  const [categoryResources, setCategoryResources] = useState(false);
  const [categoryPlatform, setCategoryPlatform] = useState(false);
  const [categoryCompany, setCategoryCompany] = useState(false);

  const resetState = useCallback((): void => {
    setCategoryResources(false);
    setCategoryServices(false);
    setCategoryPlatform(false);
    setCategoryCompany(false);
  }, []);
  const [menu, setMenu] = useState(false);
  const menuRef: RefObject<HTMLDivElement> = createRef();

  const handleClick = useCallback((): void => {
    setMenuStatus(menuStatus === 0 ? 1 : 0);
    setMenu(!menu);
    if (menu) {
      document.body.setAttribute("style", "overflow-y: auto;");
    } else {
      document.body.setAttribute("style", "overflow-y: hidden;");
    }
  }, [menu, menuStatus]);
  const handleClickButton = useCallback(
    (category: string): (() => void) =>
      (): void => {
        resetState();
        if (category === "services") {
          setCategoryServices(!categoryServices);
        } else if (category === "resources") {
          setCategoryResources(!categoryResources);
        } else if (category === "platform") {
          setCategoryPlatform(!categoryPlatform);
        } else {
          setCategoryCompany(!categoryCompany);
        }
      },
    [
      categoryServices,
      categoryResources,
      categoryCompany,
      categoryPlatform,
      resetState,
    ]
  );
  const matomoFreeTrialEvent = useCallback((): void => {
    trackEvent({ action: "free-trial-click", category: "navbar" });
  }, [trackEvent]);

  useClickOutside(menuRef, (): void => {
    resetState();
  });

  return (
    <NavbarContainer id={"navbar"} ref={menuRef}>
      <NavbarInnerContainer id={"inner_navbar"}>
        <NavbarList className={"poppins"} id={"navbar_list"}>
          <div className={"w-auto flex flex-nowrap"}>
            <li>
              <Link className={"db tc pa1 no-underline"} to={"/"}>
                <Container ph={3} pv={2} width={"160px"}>
                  <CloudImage
                    alt={"Fluid Attacks logo navbar"}
                    src={"airs/menu/Logo.png"}
                  />
                </Container>
              </Link>
            </li>
          </div>
          <Container
            center={true}
            display={width > 1240 ? "flex" : "none"}
            width={"auto"}
          >
            <Button
              onClick={handleClickButton("services")}
              size={"md"}
              variant={"ghost"}
            >
              <Text color={"#535365"}>{"Service"}</Text>
            </Button>
            <Button
              onClick={handleClickButton("platform")}
              size={"md"}
              variant={"ghost"}
            >
              <Text color={"#535365"}>{"Platform"}</Text>
            </Button>
            <AirsLink href={"/plans/"}>
              <Button size={"md"} variant={"ghost"}>
                <Text color={"#535365"}>{"Plans"}</Text>
              </Button>
            </AirsLink>
            <Button
              onClick={handleClickButton("resources")}
              size={"md"}
              variant={"ghost"}
            >
              <Text color={"#535365"}>{"Resources"}</Text>
            </Button>
            <AirsLink href={"/advisories/"}>
              <Button size={"md"} variant={"ghost"}>
                <Text color={"#535365"}>{"Advisories"}</Text>
              </Button>
            </AirsLink>
            <Button
              onClick={handleClickButton("company")}
              size={"md"}
              variant={"ghost"}
            >
              <Text color={"#535365"}>{"Company"}</Text>
            </Button>
          </Container>
          <Container
            display={width < 720 ? "none" : "flex"}
            justify={"end"}
            minWidth={"447px"}
            width={width > 1240 ? "auto" : "80%"}
            wrap={"nowrap"}
          >
            <AirsLink href={"/contact-us/"}>
              <Button variant={"secondary"}>
                <Text color={"#ffffff"}>{"Contact now"}</Text>
              </Button>
            </AirsLink>
            <Container maxWidth={"142px"} ml={2} mr={2}>
              <AirsLink href={"https://app.fluidattacks.com/SignUp"}>
                <Button onClick={matomoFreeTrialEvent} variant={"primary"}>
                  <Text color={"#ffffff"}>{"Start free trial"}</Text>
                </Button>
              </AirsLink>
            </Container>
            <AirsLink href={"https://app.fluidattacks.com/"}>
              <Button variant={"ghost"}>
                <BsFillPersonFill />
                <Text color={"#535365"}>{"Log in"}</Text>
              </Button>
            </AirsLink>
          </Container>
          <Container
            display={width < 1241 ? "flex" : "none"}
            justify={"center"}
            justifyMd={"end"}
            justifySm={"end"}
            maxWidth={width > 720 ? "50px" : "90%"}
          >
            <Button onClick={handleClick} variant={"ghost"}>
              <FiMenu size={width > 960 ? 20 : 25} />
            </Button>
          </Container>
        </NavbarList>
      </NavbarInnerContainer>
      <ServiceMenu display={categoryServices ? "flex" : "none"} />
      <PlatformMenu display={categoryPlatform ? "block" : "none"} />
      <ResourcesMenu display={categoryResources ? "block" : "none"} />
      <CompanyMenu display={categoryCompany ? "block" : "none"} />
      <DropdownMenu
        display={menu ? "block" : "none"}
        handleClick={handleClick}
        setStatus={setMenuStatus}
        status={menuStatus}
      />
    </NavbarContainer>
  );
};
