/* eslint-disable react/forbid-component-props
  -------
  We need className to override default styles from react-boostrap.
*/
import FontAwesome from "react-fontawesome";
import { LoginButton } from "scenes/Login/components/LoginButton";
import React from "react";
import _ from "lodash";
import logo from "resources/integrates.svg";
import mixpanel from "mixpanel-browser";
import style from "scenes/Login/index.css";
import { useTranslation } from "react-i18next";
import { Col, Grid, Row } from "react-bootstrap";
import {
  Col100,
  InfoButtonBitbucket,
  InfoButtonGoogle,
  InfoButtonMicrosoft,
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
    window.location.assign("/oauth/login/bitbucket-oauth2/");
  }
  function handleGoogleLogin(): void {
    mixpanel.track("Login Google");
    window.location.assign("/oauth/login/google-oauth2/");
  }
  function handleMicrosoftLogin(): void {
    mixpanel.track("Login Azure");
    window.location.assign("/oauth/login/azuread-tenant-oauth2/");
  }

  return (
    <div className={style.container}>
      <Grid>
        <Row className={style.content}>
          <Col md={4} mdOffset={4}>
            <Row>
              <img alt={"logo"} src={logo} />
            </Row>
            <Row className={"text-center"}>
              <p>{t("login.auth")}</p>
              <p>{t("login.newuser")}</p>
            </Row>
            <Row>
              <LoginButton
                className={`${style.socialBtn} ${style.googleBtn}`}
                fontAwesomeName={"google"}
                onClick={handleGoogleLogin}
                text={t("login.google")}
              />
              <LoginButton
                className={`${style.socialBtn} ${style.microsoftBtn}`}
                fontAwesomeName={"windows"}
                onClick={handleMicrosoftLogin}
                text={t("login.microsoft")}
              />
              <LoginButton
                className={`${style.socialBtn} ${style.bitbucketBtn}`}
                fontAwesomeName={"bitbucket"}
                onClick={handleBitbucketLogin}
                text={t("login.bitbucket")}
              />
            </Row>
          </Col>
        </Row>
      </Grid>
      <div className={style.deploymentDate}>
        {t("sidebar.deployment_date")}&nbsp;
        {deploymentDate}
      </div>
      <div className={style.commit}>
        {t("sidebar.commit")}&nbsp;
        <a
          href={`https://gitlab.com/fluidattacks/product/-/tree/${commitSha}`}
          rel={"noreferrer"}
          target={"_blank"}
        >
          {commitShaShort}
        </a>
      </div>
    </div>
  );
};
