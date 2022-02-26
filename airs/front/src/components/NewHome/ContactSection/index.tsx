/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";
import { useTranslation } from "react-i18next";
import {
  FaFacebookF,
  FaInstagram,
  FaLinkedinIn,
  FaTwitter,
  FaYoutube,
} from "react-icons/fa";

import {
  Container,
  InnerSection,
  SocialButton,
  SocialContainer,
  WhiteTitle,
} from "./styledComponents";

import { CloudImage } from "../../CloudImage";

const ContactSection: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  return (
    <Container>
      <InnerSection>
        <WhiteTitle>{t("contactUs.clutch")}</WhiteTitle>
        <Link
          className={"no-underline"}
          to={"https://clutch.co/profile/fluid-attacks"}
        >
          <CloudImage
            alt={"Logo OWASP"}
            src={"clutch-review"}
            styles={"tc w4 ba br3 bc-gray-64 pa2 bg-white mt3"}
          />
        </Link>
      </InnerSection>
      <InnerSection>
        <WhiteTitle>{t("contactUs.owasp")}</WhiteTitle>
        <CloudImage
          alt={"Logo OWASP"}
          src={"owasp-logo"}
          styles={"tc w4 ba bg-white br3 bc-gray-64 mt3"}
        />
      </InnerSection>
      <InnerSection>
        <WhiteTitle>{t("contactUs.lowerFollow")}</WhiteTitle>
        <SocialContainer>
          <Link
            className={"no-underline mr1"}
            to={"https://www.facebook.com/Fluid-Attacks-267692397253577/"}
          >
            <SocialButton>
              <FaFacebookF className={"f3 c-gray-64"} />
            </SocialButton>
          </Link>
          <Link
            className={"no-underline mh1"}
            to={"https://www.linkedin.com/company/fluidattacks/"}
          >
            <SocialButton>
              <FaLinkedinIn className={"f3 c-gray-64"} />
            </SocialButton>
          </Link>
          <Link
            className={"no-underline mh1"}
            to={"https://twitter.com/fluidattacks/"}
          >
            <SocialButton>
              <FaTwitter className={"f3 c-gray-64"} />
            </SocialButton>
          </Link>
          <Link
            className={"no-underline mh1"}
            to={"https://www.youtube.com/c/fluidattacks/"}
          >
            <SocialButton>
              <FaYoutube className={"f3 c-gray-64"} />
            </SocialButton>
          </Link>
          <Link
            className={"no-underline mh1"}
            to={"https://www.instagram.com/fluidattacks/"}
          >
            <SocialButton>
              <FaInstagram className={"f3 c-gray-64"} />
            </SocialButton>
          </Link>
        </SocialContainer>
      </InnerSection>
    </Container>
  );
};

export { ContactSection };
