/* eslint react/forbid-component-props: 0 */
/* eslint react/jsx-no-bind: 0 */
import { useMatomo } from "@datapunt/matomo-tracker-react";
import { Link } from "gatsby";
import React, { useCallback, useState } from "react";
import {
  BsChevronLeft,
  BsChevronRight,
  BsFillPersonFill,
} from "react-icons/bs";
import { IoMdClose } from "react-icons/io";

import { AirsLink } from "../../../components/AirsLink";
import { Button } from "../../../components/Button";
import { CloudImage } from "../../../components/CloudImage";
import { Container } from "../../../components/Container";
import type { TDisplay } from "../../../components/Container/types";
import { Text } from "../../../components/Typography";
import { useWindowSize } from "../../../utils/hooks/useWindowSize";
import { CompanyMenu } from "../Categories/Company";
import { PlatformMenu } from "../Categories/Platform";
import { ResourcesMenu } from "../Categories/Resources";
import { ServiceMenu } from "../Categories/Service";
import {
  MenuFootContainer,
  MenuMobileInnerContainer,
} from "../styles/styledComponents";

interface IServiceProps {
  display: TDisplay;
  handleClick: () => void;
}

const DropdownMenu: React.FC<IServiceProps> = ({
  display,
  handleClick,
}): JSX.Element => {
  const { width } = useWindowSize();
  const [categoryShowed, setCategoryShowed] = useState(0);
  const contents: JSX.Element[] = [
    <div key={"close"} />,
    <ServiceMenu
      display={categoryShowed === 1 ? "flex" : "none"}
      key={"services"}
    />,
    <PlatformMenu display={"block"} key={"platform"} />,
    <ResourcesMenu display={"block"} key={"resources"} />,
    <CompanyMenu display={"block"} key={"company"} />,
  ];
  const categories: string[] = [
    "none",
    "Service",
    "Platform",
    "Resources",
    "Company",
  ];

  const handleClickButton = useCallback(
    (el: number): (() => void) =>
      (): void => {
        setCategoryShowed(0);
        setCategoryShowed(el);
      },
    []
  );

  const { trackEvent } = useMatomo();

  const matomoFreeTrialEvent = useCallback((): void => {
    trackEvent({ action: "free-trial-click", category: "navbar" });
  }, [trackEvent]);

  return (
    <MenuMobileInnerContainer
      style={{ display: width < 1200 ? display : "none" }}
    >
      <Container
        align={"center"}
        display={width < 1201 ? "flex" : "none"}
        height={"100px"}
        justify={"center"}
        wrap={"wrap"}
      >
        <Container justify={"start"} width={"19%"}>
          <div className={"w-auto flex flex-nowrap"}>
            <Link className={"db tc pa1 no-underline"} to={"/"}>
              <Container width={"160px"}>
                <CloudImage
                  alt={"Fluid Attacks logo navbar"}
                  src={"logo-fluid-2022"}
                />
              </Container>
            </Link>
          </div>
        </Container>
        <Container
          align={"center"}
          display={width > 727 ? "flex" : "none"}
          justify={"end"}
          width={"68%"}
        >
          <Container
            align={"center"}
            display={width > 481 ? "flex" : "none"}
            justify={"end"}
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
        </Container>
        <Container
          align={"center"}
          display={width < 1201 ? "flex" : "none"}
          height={"auto"}
          justify={"end"}
          justifySm={"end"}
          width={width > 727 ? "5%" : "71%"}
        >
          <Button onClick={handleClick} size={"sm"} variant={"ghost"}>
            <IoMdClose size={20} />
          </Button>
        </Container>
      </Container>
      <Container
        bgColor={"#ffffff"}
        display={width < 1201 ? display : "none"}
        height={"50%"}
        position={"absolute"}
        width={"100%"}
      >
        <Container
          display={categoryShowed === 0 ? "block" : "none"}
          height={"300px"}
        >
          <Container ph={4} width={"auto"} widthSm={"100%"}>
            <Button
              display={"block"}
              onClick={handleClickButton(1)}
              variant={"ghost"}
            >
              <Container display={"flex"} width={"100%"}>
                <Container width={"98%"}>
                  <Text
                    color={"#2e2e38"}
                    display={"inline"}
                    textAlign={"start"}
                  >
                    {"Service"}
                  </Text>
                </Container>
                <Container
                  align={"center"}
                  display={"flex"}
                  minWidth={"25px"}
                  width={"2%"}
                >
                  <BsChevronRight color={"#2e2e38"} size={16} />
                </Container>
              </Container>
            </Button>
          </Container>
          <Container ph={4} width={"auto"} widthSm={"100%"}>
            <Button
              display={"block"}
              onClick={handleClickButton(2)}
              variant={"ghost"}
            >
              <Container display={"flex"} width={"100%"}>
                <Container width={"98%"}>
                  <Text
                    color={"#2e2e38"}
                    display={"inline"}
                    textAlign={"start"}
                  >
                    {"Platform"}
                  </Text>
                </Container>
                <Container
                  align={"center"}
                  display={"flex"}
                  minWidth={"25px"}
                  width={"2%"}
                >
                  <BsChevronRight color={"#2e2e38"} size={16} />
                </Container>
              </Container>
            </Button>
          </Container>
          <Container ph={4} width={"auto"} widthSm={"100%"}>
            <Button display={"block"} variant={"ghost"}>
              <Container display={"flex"} width={"100%"}>
                <Container width={"98%"}>
                  <Text
                    color={"#2e2e38"}
                    display={"inline"}
                    textAlign={"start"}
                  >
                    {"Plans"}
                  </Text>
                </Container>
              </Container>
            </Button>
          </Container>
          <Container ph={4} width={"auto"} widthSm={"100%"}>
            <Button
              display={"block"}
              onClick={handleClickButton(3)}
              variant={"ghost"}
            >
              <Container display={"flex"} width={"100%"}>
                <Container width={"98%"}>
                  <Text
                    color={"#2e2e38"}
                    display={"inline"}
                    textAlign={"start"}
                  >
                    {"Resources"}
                  </Text>
                </Container>
                <Container
                  align={"center"}
                  display={"flex"}
                  minWidth={"25px"}
                  width={"2%"}
                >
                  <BsChevronRight color={"#2e2e38"} size={16} />
                </Container>
              </Container>
            </Button>
          </Container>
          <Container ph={4} width={"auto"} widthSm={"100%"}>
            <Button display={"block"} variant={"ghost"}>
              <Container display={"flex"} width={"100%"}>
                <Container width={"98%"}>
                  <Text
                    color={"#2e2e38"}
                    display={"inline"}
                    textAlign={"start"}
                  >
                    {"Advisories"}
                  </Text>
                </Container>
              </Container>
            </Button>
          </Container>
          <Container ph={4} width={"auto"} widthSm={"100%"}>
            <Button
              display={"block"}
              onClick={handleClickButton(4)}
              variant={"ghost"}
            >
              <Container display={"flex"} width={"100%"}>
                <Container width={"98%"}>
                  <Text
                    color={"#2e2e38"}
                    display={"inline"}
                    textAlign={"start"}
                  >
                    {"Company"}
                  </Text>
                </Container>
                <Container
                  align={"center"}
                  display={"flex"}
                  minWidth={"25px"}
                  width={"2%"}
                >
                  <BsChevronRight color={"#2e2e38"} size={16} />
                </Container>
              </Container>
            </Button>
          </Container>
        </Container>
        <MenuFootContainer display={categoryShowed === 0} id={"menufoot"}>
          <Container
            align={"center"}
            bgColor={"#aaaaa"}
            display={"flex"}
            justify={"center"}
            width={"100%"}
          >
            <Container
              align={"center"}
              display={width < 728 ? "flex" : "none"}
              justify={"center"}
            >
              <Container
                align={"center"}
                display={"flex"}
                justify={"center"}
                wrap={"nowrap"}
              >
                <AirsLink href={"/contact-us/"}>
                  <Button variant={"secondary"}>{"Contact now"}</Button>
                </AirsLink>
                <Container maxWidth={"142px"} ml={3}>
                  <AirsLink href={"https://app.fluidattacks.com/SignUp"}>
                    <Button onClick={matomoFreeTrialEvent} variant={"primary"}>
                      {"Start free trial"}
                    </Button>
                  </AirsLink>
                </Container>
              </Container>
            </Container>
          </Container>
        </MenuFootContainer>
        <Container
          display={categoryShowed === 0 ? "none" : "block"}
          width={"auto"}
        >
          <Container borderBottomColor={"#2e2e38"} mb={3}>
            <Button
              icon={
                <BsChevronLeft
                  color={"#2e2e38"}
                  size={16}
                  style={{ paddingRight: "10px" }}
                />
              }
              iconSide={"left"}
              onClick={handleClickButton(0)}
              variant={"ghost"}
            >
              {categories[categoryShowed]}
            </Button>
          </Container>
          {contents[categoryShowed]}
        </Container>
      </Container>
    </MenuMobileInnerContainer>
  );
};

export { DropdownMenu };
