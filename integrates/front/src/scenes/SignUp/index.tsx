import { faCircleCheck } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { Link, useLocation } from "react-router-dom";

import { StarsFull } from "./Components/StarsFull";
import { StarsMedium } from "./Components/StarsMedium";
import type { IBenefits, IQuotes } from "./types";

import { Button } from "components/Button";
import { Carousel } from "components/Carousel";
import { Container } from "components/Container";
import { ExternalLink } from "components/ExternalLink";
import { Text } from "components/Text";
import {
  loginBitBucketLogo,
  loginGoogleLogo,
  loginMicrosoftLogo,
  signUpBGR,
  signUpLogo,
} from "resources";

export const SignUp: React.FC = (): JSX.Element => {
  const hash = useLocation();
  const { t } = useTranslation();

  useEffect((): void => {
    mixpanel.track("SignUp");
    if (hash.pathname === "/SignUp") {
      sessionStorage.setItem("trial", "true");
    } else {
      sessionStorage.removeItem("trial");
    }
  }, [hash]);

  const benefits: IBenefits[] = [
    {
      data: "Automatic SAST, DAST and SCA",
      icon: faCircleCheck,
      id: 0,
    },
    {
      data: "Continuous vulnerability reporting",
      icon: faCircleCheck,
      id: 1,
    },
    {
      data:
        "Vulnerability management in our Attack Resistance " +
        "Management platform (+ GraphQL API)",
      icon: faCircleCheck,
      id: 2,
    },
    {
      data: "Control and accelerate vulnerability remediation",
      icon: faCircleCheck,
      id: 3,
    },
    {
      data: "Integration with your CI/CD for stronger control",
      icon: faCircleCheck,
      id: 4,
    },
  ];
  const quotes: IQuotes[] = [
    {
      quote:
        "“Fluid Attacks has allowed us to have accurate information at hand, " +
        "enabling us to efficiently manage vulnerability remediation and develop " +
        "more secure software”",
      reference: "CISO/COO, Payvalida",
    },
    {
      quote: "“Their customer support and professionalism are remarkable.”",
      reference: "Development Lead, Technical Process Automation Company",
    },
    {
      quote:
        "“Their recommendations have helped us improve our overall security " +
        "at a foundational level.”",
      reference:
        "Business Intelligence & Corporate Development Director, Regional Bank",
    },
  ];

  // Event handlers
  const handleBitbucketLogin: () => void = useCallback((): void => {
    mixpanel.track("Signup Bitbucket");
    window.location.assign("/dblogin");
  }, []);
  const handleGoogleLogin: () => void = useCallback((): void => {
    mixpanel.track("Signup Google");
    window.location.assign("/dglogin");
  }, []);
  const handleMicrosoftLogin: () => void = useCallback((): void => {
    mixpanel.track("Signup Azure");
    window.location.assign("/dalogin");
  }, []);

  return (
    <Container display={"flex"} height={"100%"} width={"100%"} wrap={"wrap"}>
      <Container
        display={"flex"}
        height={"100%"}
        maxHeight={"100%"}
        scroll={"none"}
        width={"50%"}
        widthMd={"53%"}
        wrap={"wrap"}
      >
        <Container
          align={"center"}
          bgImage={`url(${signUpBGR})`}
          bgImagePos={"100% 100%"}
          display={"flex"}
          height={"100%"}
          justify={"center"}
          scroll={"none"}
          width={"105%"}
          wrap={"wrap"}
        >
          <Container
            align={"center"}
            justify={"center"}
            maxHeight={"800px"}
            pl={"20px"}
            plMd={"0px"}
            prMd={"0px"}
            widthMd={"390px"}
          >
            <Container pb={"48px"} pbMd={"10px"}>
              <Container
                letterSpacing={"2px"}
                maxWidth={"696px"}
                pt={"24px"}
                width={"100%"}
              >
                <Text bright={0} fontSize={"36px"} fw={9} tone={"light"}>
                  {t("signup.title")}
                </Text>
              </Container>
              <Container
                letterSpacing={"normal"}
                lineHeight={"23px"}
                maxWidth={"568px"}
                pt={"16px"}
                width={"100%"}
                widthMd={"85%"}
              >
                <Text bright={0} fontSize={"20px"} tone={"light"}>
                  {t("signup.subtitle")}
                </Text>
              </Container>
              {benefits.map(
                (benefit: IBenefits): JSX.Element => (
                  <Container
                    display={"flex"}
                    key={benefit.id}
                    pt={"16px"}
                    wrap={"wrap"}
                  >
                    <Container letterSpacing={"1.2px"} pr={"16px"}>
                      <FontAwesomeIcon color={"#f4f4f6"} icon={benefit.icon} />
                    </Container>
                    <Container
                      lineHeight={"21px"}
                      maxWidth={"522px"}
                      widthMd={"75%"}
                    >
                      <Text bright={0} fontSize={"16px"} tone={"light"}>
                        {benefit.data}
                      </Text>
                    </Container>
                  </Container>
                )
              )}
            </Container>
            <Container
              bgColor={"#f4f4f6"}
              borderBL={"15px"}
              borderBR={"15px"}
              borderTR={"15px"}
              borderTl={"15px"}
              heightMd={"40%"}
              width={"568px"}
              widthMd={"371px"}
            >
              <Container pl={"24px"}>
                <Carousel
                  contents={[...Array(3).keys()].map(
                    (el: number): JSX.Element => (
                      <Container
                        height={"auto"}
                        key={el}
                        pr={"24px"}
                        pt={"24px"}
                        ptMd={"24px"}
                        scroll={"none"}
                      >
                        {el === 2 ? <StarsMedium /> : <StarsFull />}
                        <Container lineHeight={"1.4"}>
                          <Text fontSize={"16px"} fw={9} tone={"dark"}>
                            {quotes[el].quote}
                          </Text>
                        </Container>
                        <Container pt={"24px"} ptMd={"20px"}>
                          <Text bright={7} fontSize={"16px"} tone={"dark"}>
                            {quotes[el].reference}
                          </Text>
                        </Container>
                      </Container>
                    )
                  )}
                  tabs={["", "", ""]}
                />
              </Container>
            </Container>
          </Container>
        </Container>
      </Container>
      <Container
        align={"center"}
        bgColor={"#ffffff"}
        display={"flex"}
        height={"100%"}
        justify={"center"}
        width={"50%"}
        widthMd={"47%"}
        wrap={"wrap"}
      >
        <Container
          align={"center"}
          display={"flex"}
          height={"700px"}
          heightMd={"643px"}
          justify={"center"}
          scroll={"none"}
          width={"473px"}
          widthMd={"350px"}
          wrap={"wrap"}
        >
          <Container
            bgImage={`url(${signUpLogo})`}
            bgImagePos={"100% 100%"}
            height={"109px"}
            width={"237px"}
          />
          <Container
            align={"center"}
            display={"flex"}
            justify={"center"}
            pt={"100px"}
            ptMd={"10px"}
            width={"403px"}
            wrap={"wrap"}
          >
            <Container>
              <Text bright={3} fontSize={"36px"} fw={9} tone={"dark"}>
                {"Sign up"}
              </Text>
            </Container>
            <Container pl={"7px"} widthMd={"0px"}>
              <Text bright={3} fontSize={"36px"} fw={9} tone={"dark"}>
                {"|"}
              </Text>
            </Container>
            <Container margin={"8px"} ptMd={"12px"}>
              <Text bright={7} fontSize={"24px"} tone={"dark"}>
                {"No credit card required."}
              </Text>
            </Container>
          </Container>
          <Container align={"center"} justify={"center"} widthMd={"350px"}>
            <Container pt={"20px"} width={"100%"}>
              <Button onClick={handleGoogleLogin} size={"lg"} variant={"input"}>
                <Container
                  align={"center"}
                  boxSizing={"border-box"}
                  display={"flex"}
                  height={"32px"}
                  justify={"center"}
                  minWidth={"310px"}
                  scroll={"none"}
                  width={"435px"}
                  widthMd={"100%"}
                  wrap={"wrap"}
                >
                  <Container
                    bgImage={`url(${loginGoogleLogo})`}
                    bgImagePos={"100% 100%"}
                    height={"24px"}
                    width={"24px"}
                  />
                  <Container minWidth={"20px"} />
                  <Container>
                    <Text bright={9} fontSize={"18px"}>
                      {"Continue with Google"}
                    </Text>
                  </Container>
                </Container>
              </Button>
            </Container>
            <Container pt={"16px"} width={"100%"}>
              <Button
                onClick={handleMicrosoftLogin}
                size={"lg"}
                variant={"input"}
              >
                <Container
                  align={"center"}
                  boxSizing={"border-box"}
                  display={"flex"}
                  height={"32px"}
                  justify={"center"}
                  minWidth={"310px"}
                  scroll={"none"}
                  width={"435px"}
                  widthMd={"100%"}
                  wrap={"wrap"}
                >
                  <Container width={"28px"} widthMd={"0px"} />
                  <Container
                    bgImage={`url(${loginMicrosoftLogo})`}
                    bgImagePos={"100% 100%"}
                    height={"24px"}
                    width={"24px"}
                  />
                  <Container minWidth={"20px"} />
                  <Container>
                    <Text bright={9} fontSize={"18px"}>
                      {"Continue with Microsoft"}
                    </Text>
                  </Container>
                </Container>
              </Button>
            </Container>
            <Container pt={"16px"} width={"100%"}>
              <Button
                onClick={handleBitbucketLogin}
                size={"lg"}
                variant={"input"}
              >
                <Container
                  align={"center"}
                  boxSizing={"border-box"}
                  display={"flex"}
                  height={"32px"}
                  justify={"center"}
                  minWidth={"310px"}
                  scroll={"none"}
                  width={"435px"}
                  widthMd={"100%"}
                  wrap={"wrap"}
                >
                  <Container width={"28px"} widthMd={"0px"} />
                  <Container
                    bgImage={`url(${loginBitBucketLogo})`}
                    bgImagePos={"100% 100%"}
                    height={"24px"}
                    width={"24px"}
                  />
                  <Container minWidth={"20px"} />
                  <Container>
                    <Text bright={9} fontSize={"18px"}>
                      {"Continue with Bitbucket"}
                    </Text>
                  </Container>
                </Container>
              </Button>
            </Container>
          </Container>

          <Container
            align={"center"}
            display={"flex"}
            pb={"63px"}
            pbMd={"15px"}
            pt={"32px"}
            ptMd={"10px"}
            wrap={"wrap"}
          >
            <Container width={"190px"}>
              <Text bright={7} fontSize={"16px"} tone={"dark"}>
                {"Already have an account?"}
                &nbsp;
              </Text>
            </Container>
            <Container borderBottom={"1.5px solid #bf0b1a"}>
              <Text fontSize={"14px"}>
                <Link to={"/"}>{"Log in"}</Link>
              </Text>
            </Container>
          </Container>
          <Container
            borderTop={"1.5px solid #b0b0bf"}
            display={"flex"}
            pt={"15px"}
            width={"473px"}
            wrap={"wrap"}
          />
          <Container
            align={"center"}
            display={"flex"}
            maxWidth={"473px"}
            textAlign={"center"}
            wrap={"wrap"}
          >
            <Text
              bright={9}
              disp={"inline"}
              fontSize={"14px"}
              ta={"center"}
              tone={"light"}
            >
              {t("login.generalData.privacy")}
              <ExternalLink href={"https://fluidattacks.com/terms-use/"}>
                {"Terms of use"}
              </ExternalLink>
              {"and"}
              <ExternalLink href={"https://fluidattacks.com/privacy/"}>
                {"Privacy policy"}
              </ExternalLink>
            </Text>
          </Container>
        </Container>
      </Container>
    </Container>
  );
};
