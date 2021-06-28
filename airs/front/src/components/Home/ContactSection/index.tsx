/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint import/no-unresolved:0 */
import {
  faFacebookF,
  faInstagram,
  faLinkedinIn,
  faTwitter,
  faYoutube,
} from "@fortawesome/free-brands-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link } from "gatsby";
import React from "react";

import {
  BlueBackground,
  Container,
  InnerSection,
  MainText,
  RedButton,
  SocialButton,
  SocialContainer,
  Title,
} from "./styledComponents";

import { translate } from "../../../utils/translations/translate";

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
                <FontAwesomeIcon
                  className={"f3 c-gray-64 mh1"}
                  icon={faFacebookF}
                />
              </SocialButton>
            </Link>
            <Link
              className={"no-underline mh1"}
              to={"https://www.linkedin.com/company/fluidattacks/"}
            >
              <SocialButton>
                <FontAwesomeIcon
                  className={"f3 c-gray-64"}
                  icon={faLinkedinIn}
                />
              </SocialButton>
            </Link>
            <Link
              className={"no-underline mh1"}
              to={"https://twitter.com/fluidattacks/"}
            >
              <SocialButton>
                <FontAwesomeIcon className={"f3 c-gray-64"} icon={faTwitter} />
              </SocialButton>
            </Link>
            <Link
              className={"no-underline mh1"}
              to={"https://www.youtube.com/c/fluidattacks/"}
            >
              <SocialButton>
                <FontAwesomeIcon className={"f3 c-gray-64"} icon={faYoutube} />
              </SocialButton>
            </Link>
            <Link
              className={"no-underline mh1"}
              to={"https://www.instagram.com/fluidattacks/"}
            >
              <SocialButton>
                <FontAwesomeIcon
                  className={"f3 c-gray-64"}
                  icon={faInstagram}
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
