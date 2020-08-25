/* eslint-disable react/forbid-component-props
  -------
  We need className to override default styles from react-boostrap.
*/
import { LoginButton } from "./components/LoginButton";
import { LoginInfoButton } from "./components/LoginInfoButton";
import React from "react";
import logo from "../../resources/integrates.svg";
import mixpanel from "mixpanel-browser";
import style from "./index.css";
import { useTranslation } from "react-i18next";
import { Col, Grid, Row } from "react-bootstrap";
import { Slide, toast } from "react-toastify";

export const Login: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  // Show 2FA Notification
  React.useEffect((): void => {
    toast.info(
      <div>
        <p>{t("login.2fa")}</p>
        <div>
          <Col md={4} xs={12}>
            <LoginInfoButton
              bsStyle={"danger"}
              fontAwesomeName={"google"}
              href={"https://bit.ly/2Gpjt6h"}
            />
          </Col>
          <Col md={4} xs={12}>
            <LoginInfoButton
              bsStyle={"primary"}
              fontAwesomeName={"windows"}
              href={"https://bit.ly/2Gp1L2X"}
            />
          </Col>
          <Col md={4} xs={12}>
            <LoginInfoButton
              bsStyle={"primary"}
              fontAwesomeName={"bitbucket"}
              href={"https://bit.ly/3it0Im7"}
            />
          </Col>
        </div>
      </div>,
      { autoClose: false, className: style.twofactor, transition: Slide }
    );
  }, [t]);

  // Event handlers
  function handleBitbucketLogin(): void {
    mixpanel.track("Login Bitbucket");
    window.location.assign("/integrates/oauth/login/bitbucket-oauth2/");
  }
  function handleGoogleLogin(): void {
    mixpanel.track("Login Google");
    window.location.assign("/integrates/oauth/login/google-oauth2/");
  }
  function handleMicrosoftLogin(): void {
    mixpanel.track("Login Azure");
    window.location.assign("/integrates/oauth/login/azuread-tenant-oauth2/");
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
                bsStyle={"danger"}
                className={`${style.socialBtn} ${style.googleBtn}`}
                fontAwesomeName={"google"}
                onClick={handleGoogleLogin}
                text={t("login.google")}
              />
              <LoginButton
                bsStyle={"primary"}
                className={`${style.socialBtn} ${style.microsoftBtn}`}
                fontAwesomeName={"windows"}
                onClick={handleMicrosoftLogin}
                text={t("login.microsoft")}
              />
              <LoginButton
                bsStyle={"primary"}
                className={`${style.socialBtn} ${style.bitbucketBtn}`}
                fontAwesomeName={"bitbucket"}
                onClick={handleBitbucketLogin}
                text={t("login.bitbucket")}
              />
            </Row>
          </Col>
        </Row>
      </Grid>
    </div>
  );
};
