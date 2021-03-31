/* eslint-disable react/forbid-component-props
  -------
  We need className to override default styles from react-boostrap.
*/

import { Col100 } from "styles/styledComponents";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import logo from "resources/integrates.svg";
import style from "scenes/Login/index.css";
import { track } from "mixpanel-browser";
import { useTranslation } from "react-i18next";
import {
  CI_COMMIT_SHA,
  CI_COMMIT_SHORT_SHA,
  INTEGRATES_DEPLOYMENT_DATE,
} from "utils/ctx";
import {
  LoginButton,
  LoginCommit,
  LoginContainer,
  LoginDeploymentDate,
  LoginGrid,
  LoginRow,
  TwoFaButton,
  TwoFacol,
} from "./components";
import React, { useEffect } from "react";
import { Slide, toast } from "react-toastify";
import {
  faBitbucket,
  faGoogle,
  faWindows,
} from "@fortawesome/free-brands-svg-icons";

export const Login: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  // Event handlers 2FA notification Buttons
  function handleNotificationGoogle(): void {
    location.assign("https://bit.ly/2Gpjt6h");
  }
  function handleNotificationMicrosoft(): void {
    location.assign("https://bit.ly/2Gp1L2X");
  }
  function handleNotificationBitbucket(): void {
    location.assign("https://bit.ly/3it0Im7");
  }

  // Show 2FA Notification
  useEffect((): void => {
    toast.info(
      <div className={"pa1-ns"}>
        <div className={style.twoP}>
          <Col100>
            <p className={"mt1"}>{t("login.2fa")}</p>
          </Col100>
        </div>
        <div className={"flex"}>
          <TwoFacol>
            <TwoFaButton
              className={"btn-google"}
              icon={<FontAwesomeIcon icon={faGoogle} size={"2x"} />}
              onClick={handleNotificationGoogle}
            />
          </TwoFacol>
          <TwoFacol>
            <TwoFaButton
              className={"btn-azure"}
              icon={<FontAwesomeIcon icon={faWindows} size={"2x"} />}
              onClick={handleNotificationMicrosoft}
            />
          </TwoFacol>
          <TwoFacol>
            <TwoFaButton
              className={"btn-bitbucket"}
              icon={<FontAwesomeIcon icon={faBitbucket} size={"2x"} />}
              onClick={handleNotificationBitbucket}
            />
          </TwoFacol>
        </div>
      </div>,
      { autoClose: false, className: style.twofactor, transition: Slide }
    );
  }, [t]);

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
        <LoginRow>
          <img alt={"logo"} src={logo} />
        </LoginRow>
        <LoginRow>
          <p className={"mt0"}>{t("login.auth")}</p>
          <p className={"mt0"}>{t("login.newuser")}</p>
        </LoginRow>
        <LoginRow>
          <LoginButton
            className={"btn-lgoogle"}
            icon={<FontAwesomeIcon icon={faGoogle} size={"2x"} />}
            id={"login-google"}
            onClick={handleGoogleLogin}
            text={t("login.google")}
          />
          <LoginButton
            className={"btn-lazure"}
            icon={<FontAwesomeIcon icon={faWindows} size={"2x"} />}
            id={"login-microsoft"}
            onClick={handleMicrosoftLogin}
            text={t("login.microsoft")}
          />
          <LoginButton
            className={"btn-lbitbucket"}
            icon={<FontAwesomeIcon icon={faBitbucket} size={"2x"} />}
            id={"login-bitbucket"}
            onClick={handleBitbucketLogin}
            text={t("login.bitbucket")}
          />
        </LoginRow>
      </LoginGrid>
      <LoginDeploymentDate>
        {t("sidebar.deploymentDate")}&nbsp;
        {INTEGRATES_DEPLOYMENT_DATE}
      </LoginDeploymentDate>
      <LoginCommit>
        {t("sidebar.commit")}&nbsp;
        <a
          href={`https://gitlab.com/fluidattacks/product/-/tree/${CI_COMMIT_SHA}`}
          rel={"noreferrer"}
          target={"_blank"}
        >
          {CI_COMMIT_SHORT_SHA}
        </a>
      </LoginCommit>
    </LoginContainer>
  );
};
