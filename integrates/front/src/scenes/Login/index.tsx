/* eslint-disable react/forbid-component-props
  -------
  We need className to override default styles from react-boostrap.
*/

import { faBitbucket, faWindows } from "@fortawesome/free-brands-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useEffect } from "react";
import { useTranslation } from "react-i18next";
import { useLocation } from "react-router-dom";

import { LoginButton, LoginContainer, LoginGrid } from "./components";

import { ExternalLink } from "components/ExternalLink";
import google from "resources/google.svg";
import logo from "resources/logo.svg";
import style from "scenes/Login/index.css";
import {
  CI_COMMIT_SHA,
  CI_COMMIT_SHORT_SHA,
  INTEGRATES_DEPLOYMENT_DATE,
} from "utils/ctx";

export const Login: React.FC = (): JSX.Element => {
  const { hash } = useLocation();
  const { t } = useTranslation();

  useEffect((): void => {
    if (hash === "#trial") {
      sessionStorage.setItem("trial", "true");
    } else {
      sessionStorage.removeItem("trial");
    }
  }, [hash]);

  // Event handlers
  function handleBitbucketLogin(): void {
    mixpanel.track("Login Bitbucket");
    window.location.assign("/dblogin");
  }
  function handleGoogleLogin(): void {
    mixpanel.track("Login Google");
    window.location.assign("/dglogin");
  }
  function handleMicrosoftLogin(): void {
    mixpanel.track("Login Azure");
    window.location.assign("/dalogin");
  }

  return (
    <LoginContainer>
      <LoginGrid>
        <img alt={"logo"} className={style.logo} src={logo} />
        <p className={`tc mt4 mb4 ${style["text-color"]}`} id={"login-auth"}>
          {t("login.auth")}
        </p>
        <LoginButton
          className={"btn-lgoogle mb2 black"}
          icon={
            <img alt={"google"} className={style["ico-google"]} src={google} />
          }
          id={"login-google"}
          onClick={handleGoogleLogin}
          text={t("login.google")}
        />
        <LoginButton
          className={"btn-lazure mb2 white"}
          icon={
            <FontAwesomeIcon
              className={"f3"}
              fixedWidth={true}
              icon={faWindows}
            />
          }
          id={"login-microsoft"}
          onClick={handleMicrosoftLogin}
          text={t("login.microsoft")}
        />
        <LoginButton
          className={"btn-lbitbucket mb0 white"}
          icon={
            <FontAwesomeIcon
              className={"f3"}
              fixedWidth={true}
              icon={faBitbucket}
            />
          }
          id={"login-bitbucket"}
          onClick={handleBitbucketLogin}
          text={t("login.bitbucket")}
        />
        <div className={`mb0 tc ${style["text-color"]}`}>
          <p>
            <ExternalLink href={"https://fluidattacks.com/terms-use/"}>
              {t("login.termsOfUseLinkText")}
            </ExternalLink>
            {"|"}
            <ExternalLink href={"https://fluidattacks.com/privacy/"}>
              {t("login.privacyLinkText")}
            </ExternalLink>
          </p>
          <p className={"mb0"}>
            {t("info.deploymentDate")}&nbsp;
            {INTEGRATES_DEPLOYMENT_DATE}
          </p>
          <ExternalLink
            className={style["link-default"]}
            href={`https://gitlab.com/fluidattacks/universe/-/tree/${CI_COMMIT_SHA}`}
          >
            {t("info.commit")}&nbsp;
            {CI_COMMIT_SHORT_SHA}
          </ExternalLink>
        </div>
      </LoginGrid>
    </LoginContainer>
  );
};
