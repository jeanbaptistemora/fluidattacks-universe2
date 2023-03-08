/* eslint react/forbid-component-props: 0 */
import { useMatomo } from "@datapunt/matomo-tracker-react";
import { Link } from "gatsby";
import React, { createRef, useCallback, useState } from "react";
import type { RefObject } from "react";
import { BsFillPersonFill } from "react-icons/bs";
import { FiMenu } from "react-icons/fi";
import { useWindowSize } from "usehooks-ts";

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
import {
  NavbarInnerContainer,
  NavbarList,
} from "../../styles/styledComponents";

export const NavbarComponent: React.FC = (): JSX.Element => {
  const { trackEvent } = useMatomo();
  const { width } = useWindowSize();
  const [menuStatus, setMenuStatus] = useState(0);
  const [categoryShown, setCategoryShown] = useState(0);

  const handleScreen = useCallback((): string => {
    if (width < 1241 && width > 720) {
      return "medium";
    } else if (width < 720 && width > 10) {
      return "mobile";
    }

    return "desktop";
  }, [width]);
  const screen = handleScreen();
  const resetState = useCallback((): void => {
    setCategoryShown(0);
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
  const contents: JSX.Element[] = [
    <div key={"close"} />,
    <ServiceMenu display={"block"} key={"services"} />,
    <PlatformMenu display={"block"} key={"platform"} />,
    <ResourcesMenu display={"block"} key={"resources"} />,
    <CompanyMenu display={"block"} key={"company"} />,
  ];
  const handleClickButton = useCallback(
    (category: string): (() => void) =>
      (): void => {
        resetState();
        if (category === "services") {
          setCategoryShown(1);
        } else if (category === "resources") {
          setCategoryShown(3);
        } else if (category === "platform") {
          setCategoryShown(2);
        } else {
          setCategoryShown(4);
        }
      },
    [resetState]
  );
  const matomoFreeTrialEvent = useCallback((): void => {
    trackEvent({ action: "free-trial-click", category: "navbar" });
  }, [trackEvent]);

  useClickOutside(menuRef, (): void => {
    resetState();
  });
  handleScreen();

  if (screen === "mobile") {
    return (
      <NavbarContainer id={"navbar"} ref={menuRef}>
        <NavbarInnerContainer id={"inner_navbar"}>
          <NavbarList className={"poppins"} id={"navbar_list"}>
            <div className={"w-auto flex flex-nowrap"}>
              <li>
                <Link className={"db tc pa1 no-underline"} to={"/"}>
                  <Container display={"block"} ph={3} pv={2} width={"160px"}>
                    <CloudImage
                      alt={"Fluid Attacks logo navbar"}
                      src={"airs/menu/Logo.png"}
                    />
                  </Container>
                </Link>
              </li>
            </div>
            <Container
              display={"flex"}
              justify={"center"}
              justifyMd={"end"}
              justifySm={"end"}
              maxWidth={"90%"}
            >
              <Button onClick={handleClick} variant={"ghost"}>
                <FiMenu size={width > 960 ? 20 : 25} />
              </Button>
            </Container>
          </NavbarList>
        </NavbarInnerContainer>
        {contents[categoryShown]}
        <DropdownMenu
          display={menu ? "block" : "none"}
          handleClick={handleClick}
          setStatus={setMenuStatus}
          status={menuStatus}
        />
      </NavbarContainer>
    );
  } else if (screen === "medium") {
    return (
      <NavbarContainer id={"navbar"} ref={menuRef}>
        <NavbarInnerContainer id={"inner_navbar"}>
          <NavbarList className={"poppins"} id={"navbar_list"}>
            <div className={"w-auto flex flex-nowrap"}>
              <li>
                <Link className={"db tc pa1 no-underline"} to={"/"}>
                  <Container display={"block"} ph={3} pv={2} width={"160px"}>
                    <CloudImage
                      alt={"Fluid Attacks logo navbar"}
                      src={"airs/menu/Logo.png"}
                    />
                  </Container>
                </Link>
              </li>
            </div>
            <Container
              display={"flex"}
              justify={"end"}
              minWidth={"447px"}
              width={"80%"}
              wrap={"nowrap"}
            >
              <AirsLink href={"/contact-us/"}>
                <Button variant={"secondary"}>{"Contact now"}</Button>
              </AirsLink>
              <Container maxWidth={"142px"} ml={2} mr={2}>
                <AirsLink href={"https://app.fluidattacks.com/SignUp"}>
                  <Button onClick={matomoFreeTrialEvent} variant={"primary"}>
                    {"Start free trial"}
                  </Button>
                </AirsLink>
              </Container>
              <AirsLink href={"https://app.fluidattacks.com/"}>
                <Button variant={"ghost"}>
                  <BsFillPersonFill />
                  {"Log in"}
                </Button>
              </AirsLink>
            </Container>
            <Container
              display={"flex"}
              justify={"center"}
              justifyMd={"end"}
              justifySm={"end"}
              maxWidth={"50px"}
            >
              <Button onClick={handleClick} variant={"ghost"}>
                <FiMenu size={width > 960 ? 20 : 25} />
              </Button>
            </Container>
          </NavbarList>
        </NavbarInnerContainer>
        {contents[categoryShown]}
        <DropdownMenu
          display={menu ? "block" : "none"}
          handleClick={handleClick}
          setStatus={setMenuStatus}
          status={menuStatus}
        />
      </NavbarContainer>
    );
  }

  return (
    <NavbarContainer id={"navbar"} ref={menuRef}>
      <NavbarInnerContainer id={"inner_navbar"}>
        <NavbarList className={"poppins"} id={"navbar_list"}>
          <div className={"w-auto flex flex-nowrap"}>
            <li>
              <Link className={"db tc pa1 no-underline"} to={"/"}>
                <Container display={"block"} ph={3} pv={2} width={"160px"}>
                  <CloudImage
                    alt={"Fluid Attacks logo navbar"}
                    src={"airs/menu/Logo.png"}
                  />
                </Container>
              </Link>
            </li>
          </div>
          <Container center={true} display={"flex"} width={"auto"}>
            <Button
              onClick={handleClickButton("services")}
              size={"md"}
              variant={"ghost"}
            >
              {"Service"}
            </Button>
            <Button
              onClick={handleClickButton("platform")}
              size={"md"}
              variant={"ghost"}
            >
              {"Platform"}
            </Button>
            <AirsLink href={"/plans/"}>
              <Button size={"md"} variant={"ghost"}>
                {"Plans"}
              </Button>
            </AirsLink>
            <Button
              onClick={handleClickButton("resources")}
              size={"md"}
              variant={"ghost"}
            >
              {"Resources"}
            </Button>
            <AirsLink href={"/advisories/"}>
              <Button size={"md"} variant={"ghost"}>
                {"Advisories"}
              </Button>
            </AirsLink>
            <Button
              onClick={handleClickButton("company")}
              size={"md"}
              variant={"ghost"}
            >
              {"Company"}
            </Button>
          </Container>
          <Container
            display={"flex"}
            justify={"end"}
            minWidth={"447px"}
            width={"auto"}
            wrap={"nowrap"}
          >
            <AirsLink href={"/contact-us/"}>
              <Button variant={"secondary"}>{"Contact now"}</Button>
            </AirsLink>
            <Container maxWidth={"142px"} ml={2} mr={2}>
              <AirsLink href={"https://app.fluidattacks.com/SignUp"}>
                <Button onClick={matomoFreeTrialEvent} variant={"primary"}>
                  {"Start free trial"}
                </Button>
              </AirsLink>
            </Container>
            <AirsLink href={"https://app.fluidattacks.com/"}>
              <Button variant={"ghost"}>
                <BsFillPersonFill />
                {"Log in"}
              </Button>
            </AirsLink>
          </Container>
        </NavbarList>
      </NavbarInnerContainer>
      {contents[categoryShown]}
    </NavbarContainer>
  );
};
