/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint import/no-unresolved:0 */
import { Link } from "gatsby";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";
import { translate } from "../../../utils/translations/translate";
import * as facebookIcon from "../../../../static/images/footer/icon-fb-dark.svg";
import * as instagramIcon from "../../../../static/images/footer/icon-ig-dark.svg";
import * as linkedinIcon from "../../../../static/images/footer/icon-linkedin-dark.svg";
import * as twitterIcon from "../../../../static/images/footer/icon-tw-dark.svg";
import * as youtubeIcon from "../../../../static/images/footer/icon-yt-dark.svg";

const BlueBackground: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    bg-darker-blue
  `,
})``;
const Container: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    h-400
    mw-1366
    center
    ph-body
    pv5
    bg-darker-blue
  `,
})``;

const Title: StyledComponent<"p", Record<string, unknown>> = styled.p.attrs({
  className: `
    tl
    roboto
    c-black-gray
    f5
    mh0
  `,
})``;

const MainText: StyledComponent<"p", Record<string, unknown>> = styled.p.attrs({
  className: `
    neue
    f3
    tl
    fw7
    c-fluid-gray
  `,
})``;

const InnerSection: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w5-l
  `,
})``;

const RedButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    w-auto-l
    w-100
    outline-transparent
    bg-button-red
    hv-bg-fluid-rd
    pointer
    white
    pv3
    ph5
    fw4
    f5
    dib
    t-all-3-eio
    br2
    bc-fluid-red
    ba
  `,
})``;

const SocialContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    flex
    mt4
    pt3
  `,
})``;

const SocialButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    pa2
    ba
    br3
    bc-gray-64
    bg-transparent
    pointer
  `,
})``;

const ContactSection: React.FC = (): JSX.Element => (
  <BlueBackground>
    <Container>
      <Title>{translate.t("contactUs.subTitle")}</Title>
      <div className={"flex-l"}>
        <InnerSection className={"ml0-l mr-auto-l center"}>
          <MainText>{translate.t("contactUs.formMessage")}</MainText>
          <Link className={"no-underline"} to={"/contact-us/"}>
            <RedButton>{translate.t("contactUs.formButton")}</RedButton>
          </Link>
        </InnerSection>
        <InnerSection>
          <MainText>{translate.t("contactUs.subscribeMessage")}</MainText>
          <Link className={"no-underline"} to={"/subscription/"}>
            <RedButton>{"Subscribe"}</RedButton>
          </Link>
        </InnerSection>
        <InnerSection className={"mr0-l ml-auto-l center"}>
          <MainText>{translate.t("contactUs.follow")}</MainText>
          <SocialContainer>
            <Link
              className={"no-underline mr1"}
              to={"https://www.facebook.com/Fluid-Attacks-267692397253577/"}
            >
              <SocialButton>
                <img
                  alt={"Facebook Icon"}
                  className={"w3"}
                  src={facebookIcon}
                />
              </SocialButton>
            </Link>
            <Link
              className={"no-underline mh1"}
              to={"https://www.linkedin.com/company/fluidattacks/"}
            >
              <SocialButton>
                <img
                  alt={"LinkedIn Icon"}
                  className={"w3"}
                  src={linkedinIcon}
                />
              </SocialButton>
            </Link>
            <Link
              className={"no-underline mh1"}
              to={"https://twitter.com/fluidattacks/"}
            >
              <SocialButton>
                <img alt={"Twitter Icon"} className={"w3"} src={twitterIcon} />
              </SocialButton>
            </Link>
            <Link
              className={"no-underline mh1"}
              to={"https://www.youtube.com/c/fluidattacks/"}
            >
              <SocialButton>
                <img alt={"Youtube Icon"} className={"w3"} src={youtubeIcon} />
              </SocialButton>
            </Link>
            <Link
              className={"no-underline mh1"}
              to={"https://www.instagram.com/fluidattacks/"}
            >
              <SocialButton>
                <img
                  alt={"Instagram Icon"}
                  className={"w3"}
                  src={instagramIcon}
                />
              </SocialButton>
            </Link>
          </SocialContainer>
        </InnerSection>
      </div>
    </Container>
  </BlueBackground>
);

export { ContactSection };
