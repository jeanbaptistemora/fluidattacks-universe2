/* eslint-disable react/forbid-component-props
  -------
  We need className to override default styles from react-boostrap.
*/
import FontAwesome from "react-fontawesome";
import React from "react";
import _ from "lodash";
import logo from "resources/integrates.svg";
import mixpanel from "mixpanel-browser";
import style from "scenes/Login/index.css";
import { useTranslation } from "react-i18next";
import {
  Col100,
  InfoButtonBitbucket,
  InfoButtonGoogle,
  InfoButtonMicrosoft,
  LoginButtonBitbucket,
  LoginButtonGoogle,
  LoginButtonMicrosoft,
  LoginCommit,
  LoginContainer,
  LoginDeploymentDate,
  LoginGrid,
  LoginRow,
  Notification2FaCol,
  Notification2FaGrid,
  Notification2FaRow,
} from "styles/styledComponents";
import { Slide, toast } from "react-toastify";

export const Login: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const deploymentDate: string = _.isString(
    process.env.INTEGRATES_DEPLOYMENT_DATE
  )
    ? process.env.INTEGRATES_DEPLOYMENT_DATE
    : "";
  const commitSha: string = _.isString(process.env.CI_COMMIT_SHA)
    ? process.env.CI_COMMIT_SHA
    : "";
  const commitShaShort: string = _.isString(process.env.CI_COMMIT_SHORT_SHA)
    ? process.env.CI_COMMIT_SHORT_SHA
    : "";

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
  React.useEffect((): void => {
    toast.info(
      <Notification2FaGrid>
        <Notification2FaRow>
          <Col100>
            <p>{t("login.2fa")}</p>
          </Col100>
        </Notification2FaRow>
        <Notification2FaRow>
          <Notification2FaCol>
            <InfoButtonGoogle onClick={handleNotificationGoogle}>
              <span>
                <FontAwesome name={"google"} size={"2x"} />
              </span>
            </InfoButtonGoogle>
          </Notification2FaCol>
          <Notification2FaCol>
            <InfoButtonMicrosoft onClick={handleNotificationMicrosoft}>
              <span>
                <FontAwesome name={"windows"} size={"2x"} />
              </span>
            </InfoButtonMicrosoft>
          </Notification2FaCol>
          <Notification2FaCol>
            <InfoButtonBitbucket onClick={handleNotificationBitbucket}>
              <span>
                <FontAwesome name={"bitbucket"} size={"2x"} />
              </span>
            </InfoButtonBitbucket>
          </Notification2FaCol>
        </Notification2FaRow>
      </Notification2FaGrid>,
      { autoClose: false, className: style.twofactor, transition: Slide }
    );
  }, [t]);

  // Event handlers
  function handleBitbucketLogin(): void {
    mixpanel.track("Login Bitbucket");
    window.location.assign("/new/dblogin");
  }
  function handleGoogleLogin(): void {
    mixpanel.track("Login Google");
    window.location.assign("/new/dglogin");
  }
  function handleMicrosoftLogin(): void {
    mixpanel.track("Login Azure");
    window.location.assign("/new/dalogin");
  }

  return (
    <LoginContainer>
      <LoginGrid>
        <LoginRow>
          <img alt={"logo"} src={logo} />
        </LoginRow>
        <LoginRow>
          <p>{t("login.auth")}</p>
          <p>{t("login.newuser")}</p>
        </LoginRow>
        <LoginRow>
          <LoginButtonGoogle onClick={handleGoogleLogin}>
            <FontAwesome name={"google"} size={"2x"} />
            {t("login.google")}
          </LoginButtonGoogle>
          <LoginButtonMicrosoft onClick={handleMicrosoftLogin}>
            <FontAwesome name={"windows"} size={"2x"} />
            {t("login.microsoft")}
          </LoginButtonMicrosoft>
          <LoginButtonBitbucket onClick={handleBitbucketLogin}>
            <FontAwesome name={"bitbucket"} size={"2x"} />
            {t("login.bitbucket")}
          </LoginButtonBitbucket>
        </LoginRow>
      </LoginGrid>
      <LoginDeploymentDate>
        {t("sidebar.deployment_date")}&nbsp;
        {deploymentDate}
      </LoginDeploymentDate>
      <LoginCommit>
        {t("sidebar.commit")}&nbsp;
        <a
          href={`https://gitlab.com/fluidattacks/product/-/tree/${commitSha}`}
          rel={"noreferrer"}
          target={"_blank"}
        >
          {commitShaShort}
        </a>
      </LoginCommit>
    </LoginContainer>
  );
};
