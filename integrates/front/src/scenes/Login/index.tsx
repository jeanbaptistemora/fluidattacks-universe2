// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { Link, useLocation } from "react-router-dom";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { ExternalLink } from "components/ExternalLink";
import { Tag } from "components/Tag";
import { Text } from "components/Text";
import {
  loginBGR,
  loginBitBucketLogo,
  loginGoogleLogo,
  loginLogo,
  loginMicrosoftLogo,
  loginNewFeat,
} from "resources";

export const Login: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const hash = useLocation();
  useEffect((): void => {
    mixpanel.track("LogIn");
    if (hash.pathname === "/SignUp") {
      sessionStorage.setItem("trial", "true");
    } else {
      sessionStorage.removeItem("trial");
    }
  }, [hash]);

  // Event handlers
  const handleBitbucketLogin: () => void = useCallback((): void => {
    mixpanel.track("Login Bitbucket");
    window.location.assign("/dblogin");
  }, []);
  const handleGoogleLogin: () => void = useCallback((): void => {
    mixpanel.track("Login Google");
    window.location.assign("/dglogin");
  }, []);
  const handleMicrosoftLogin: () => void = useCallback((): void => {
    mixpanel.track("Login Azure");
    window.location.assign("/dalogin");
  }, []);

  return (
    <Container display={"flex"} height={"100%"} width={"100%"} wrap={"wrap"}>
      <Container
        align={"center"}
        bgColor={"#ffffff"}
        display={"flex"}
        height={"100%"}
        justify={"center"}
        width={"33%"}
        wrap={"wrap"}
      >
        <Container
          align={"center"}
          display={"flex"}
          height={"700px"}
          heightMd={"643px"}
          justify={"center"}
          maxWidth={"390px"}
          position={"absolute"}
          scroll={"none"}
          width={"100%"}
          widthMd={"30%"}
          wrap={"wrap"}
        >
          <Container
            align={"center"}
            display={"flex"}
            justify={"center"}
            width={"390px"}
            wrap={"wrap"}
          >
            <Container
              bgImage={`url(${loginLogo})`}
              bgImagePos={"100% 100%"}
              height={"109px"}
              width={"237px"}
            />
          </Container>

          <Container
            align={"center"}
            display={"flex"}
            justify={"center"}
            pt={"100px"}
            ptMd={"50px"}
            width={"390px"}
            wrap={"wrap"}
          >
            <Container id={"login-auth"}>
              <Text fontSize={"36px"} fw={9} tone={"dark"}>
                {"Log in"}
              </Text>
            </Container>
          </Container>
          <Container
            maxWidth={"390px"}
            pt={"32px"}
            scroll={"none"}
            widthMd={"300px"}
          >
            <Button onClick={handleGoogleLogin} size={"lg"} variant={"input"}>
              <Container
                align={"center"}
                display={"flex"}
                justify={"center"}
                width={"350px"}
                widthMd={"100%"}
                wrap={"wrap"}
              >
                <Container width={"40px"} widthMd={"0px"} />
                <Container
                  bgImage={`url(${loginGoogleLogo})`}
                  bgImagePos={"100% 100%"}
                  height={"24px"}
                  width={"24px"}
                />
                <Container minWidth={"20px"} />
                <Container pt={"2px"} width={"200px"}>
                  <Text bright={9} fontSize={"18px"}>
                    {"Continue with Google"}
                  </Text>
                </Container>
              </Container>
            </Button>
          </Container>
          <Container
            maxWidth={"390px"}
            pt={"16px"}
            ptMd={"0px"}
            scroll={"none"}
            widthMd={"300px"}
          >
            <Button
              onClick={handleMicrosoftLogin}
              size={"lg"}
              variant={"input"}
            >
              <Container
                align={"center"}
                display={"flex"}
                justify={"center"}
                width={"350px"}
                widthMd={"100%"}
                wrap={"wrap"}
              >
                <Container width={"40px"} widthMd={"0px"} />
                <Container
                  bgImage={`url(${loginMicrosoftLogo})`}
                  bgImagePos={"100% 100%"}
                  height={"24px"}
                  pl={"20px"}
                  width={"24px"}
                />
                <Container minWidth={"20px"} />
                <Container pt={"2px"} width={"200px"}>
                  <Text bright={9} fontSize={"18px"}>
                    {"Continue with Microsoft"}
                  </Text>
                </Container>
              </Container>
            </Button>
          </Container>
          <Container
            maxWidth={"390px"}
            pt={"16px"}
            ptMd={"0px"}
            scroll={"none"}
            widthMd={"300px"}
          >
            <Button
              onClick={handleBitbucketLogin}
              size={"lg"}
              variant={"input"}
            >
              <Container
                align={"center"}
                display={"flex"}
                justify={"center"}
                width={"350px"}
                widthMd={"100%"}
                wrap={"wrap"}
              >
                <Container width={"40px"} widthMd={"0px"} />
                <Container
                  bgImage={`url(${loginBitBucketLogo})`}
                  bgImagePos={"100% 100%"}
                  height={"24px"}
                  pl={"20px"}
                  width={"24px"}
                />
                <Container minWidth={"20px"} />
                <Container pt={"2px"} width={"200px"}>
                  <Text bright={9} fontSize={"18px"}>
                    {"Continue with Bitbucket"}
                  </Text>
                </Container>
              </Container>
            </Button>
          </Container>
          <Container
            align={"center"}
            display={"flex"}
            justify={"center"}
            pb={"60px"}
            pbMd={"10px"}
            pt={"32px"}
            width={"350px"}
            wrap={"wrap"}
          >
            <Container width={"169px"}>
              <Text bright={7} fontSize={"16px"} tone={"dark"}>
                {"Don't have an account?"}
                &nbsp;
              </Text>
            </Container>
            <Container borderBottom={"1.5px solid #bf0b1a"}>
              <Text fontSize={"14px"}>
                <Link to={"/SignUp"}>{"Sign Up"}</Link>
              </Text>
            </Container>
          </Container>
          <Container
            align={"center"}
            borderTop={"1.5px solid #b0b0bf"}
            display={"inline"}
            justify={"center"}
            pt={"15px"}
            width={"350px"}
          >
            <Text bright={9} fontSize={"14px"} ta={"center"} tone={"light"}>
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
          <Container
            align={"center"}
            display={"flex"}
            justify={"center"}
            width={"350px"}
          />
        </Container>
      </Container>
      <Container
        display={"flex"}
        height={"100%"}
        maxHeight={"100%"}
        scroll={"none"}
        width={"67%"}
        wrap={"wrap"}
      >
        <Container
          align={"center"}
          bgImage={`url(${loginBGR})`}
          bgImagePos={"100% 100%"}
          display={"flex"}
          height={"100%"}
          justify={"center"}
          scroll={"none"}
          width={"100%"}
          wrap={"wrap"}
        >
          <Container
            display={"flex"}
            heightMd={"90%"}
            maxHeight={"740px"}
            maxWidth={"696px"}
            widthMd={"90%"}
            wrap={"wrap"}
          >
            <Container maxHeight={"70px"} ptMd={"15px"}>
              <Tag variant={"redNoBd"}>
                <Container
                  height={"30px"}
                  maxHeight={"37px"}
                  pt={"7px"}
                  width={"108px"}
                >
                  <Text fontSize={"16px"} fw={9} ta={"center"} tone={"red"}>
                    {t("login.generalData.newFeature")}
                  </Text>
                </Container>
              </Tag>
            </Container>

            <Container
              maxWidth={"696px"}
              pt={"24px"}
              ptMd={"0px"}
              width={"100%"}
            >
              <Text fontSize={"24px"} fw={9} tone={"light"}>
                {t("login.generalData.subtitle")}
              </Text>
            </Container>
            <Container
              maxWidth={"696px"}
              pb={"30px"}
              pbMd={"0px"}
              pt={"24px"}
              ptMd={"0px"}
              width={"100%"}
            >
              <Text bright={6} fontSize={"16px"} tone={"light"}>
                {t("login.generalData.description")}
              </Text>
            </Container>
            <Container
              align={"start"}
              bgImage={`url(${loginNewFeat})`}
              bgImagePos={"100% 100%"}
              borderBL={"10px"}
              borderBR={"10px"}
              borderTR={"10px"}
              borderTl={"10px"}
              height={"370px"}
              heightMd={"43%"}
              width={"620px"}
              widthMd={"90%"}
            />
          </Container>
        </Container>
      </Container>
    </Container>
  );
};
