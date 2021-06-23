/* eslint-disable react/forbid-component-props
  -------
  We need className to override default styles from react-boostrap.
*/

import {
  faBitbucket,
  faGoogle,
  faWindows,
} from "@fortawesome/free-brands-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { track } from "mixpanel-browser";
import React from "react";
import { useTranslation } from "react-i18next";

import { LoginButton, LoginContainer, LoginGrid } from "./components";

import logo from "resources/asm.svg";
import style from "scenes/Login/index.css";
import {
  CI_COMMIT_SHA,
  CI_COMMIT_SHORT_SHA,
  INTEGRATES_DEPLOYMENT_DATE,
} from "utils/ctx";

export const Login: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  // Event handlers
  function handleBitbucketLogin(): void {
    track("Login Bitbucket");
    window.location.assign("/dblogin");
  }
  function handleGoogleLogin(): void {
    track("Login Google");
    window.location.assign("/dglogin");
  }
  function handleMicrosoftLogin(): void {
    track("Login Azure");
    window.location.assign("/dalogin");
  }

  return (
    <LoginContainer>
      <LoginGrid>
        <img alt={"logo"} className={style.logo} src={logo} />
        <p className={`tc mt4 mb4 ${style["text-color"]}`}>{t("login.auth")}</p>
        <LoginButton
          className={"btn-lgoogle mb2"}
          icon={
            <FontAwesomeIcon
              className={"f3"}
              fixedWidth={true}
              icon={faGoogle}
            />
          }
          id={"login-google"}
          onClick={handleGoogleLogin}
          text={t("login.google")}
        />
        <LoginButton
          className={"btn-lazure mb2"}
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
          className={"btn-lbitbucket mb0"}
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
        <div className={`mt4 mb0 tc ${style["text-color"]}`}>
          <p className={"mb0"}>
            {t("info.deploymentDate")}&nbsp;
            {INTEGRATES_DEPLOYMENT_DATE}
          </p>
          <a
            className={style["link-default"]}
            href={`https://gitlab.com/fluidattacks/product/-/tree/${CI_COMMIT_SHA}`}
            rel={"noreferrer"}
            target={"_blank"}
          >
            {t("info.commit")}&nbsp;
            {CI_COMMIT_SHORT_SHA}
          </a>
        </div>
      </LoginGrid>
    </LoginContainer>
  );
};
