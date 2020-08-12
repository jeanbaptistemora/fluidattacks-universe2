/* eslint-disable react/forbid-component-props
  -------
  We need className to override default styles from react-boostrap.
*/
import FontAwesome from "react-fontawesome";
import React from "react";
import { default as logo } from "../../resources/integrates.svg";
import mixpanel from "mixpanel-browser";
import { default as style } from "./index.css";
import { useTranslation } from "react-i18next";
import { Button, Col, Grid, Row } from "react-bootstrap";
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
            <Button
              block={true}
              bsStyle={"danger"}
              href={"https://bit.ly/2Gpjt6h"}
            >
              <FontAwesome name={"google"} size={"2x"} />
              &nbsp;
            </Button>
          </Col>
          <Col md={4} xs={12}>
            <Button
              block={true}
              bsStyle={"primary"}
              href={"https://bit.ly/2Gp1L2X"}
            >
              <FontAwesome name={"windows"} size={"2x"} />
              &nbsp;
            </Button>
          </Col>
          <Col md={4} xs={12}>
            <Button
              block={true}
              bsStyle={"primary"}
              href={"https://bit.ly/3it0Im7"}
            >
              <FontAwesome name={"bitbucket"} size={"2x"} />
              &nbsp;
            </Button>
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
              <Button
                block={true}
                bsStyle={"danger"}
                className={`${style.socialBtn} ${style.googleBtn}`}
                onClick={handleGoogleLogin}
              >
                <FontAwesome name={"google"} size={"2x"} />
                {t("login.google")}
              </Button>
              <Button
                block={true}
                bsStyle={"primary"}
                className={`${style.socialBtn} ${style.microsoftBtn}`}
                onClick={handleMicrosoftLogin}
              >
                <FontAwesome name={"windows"} size={"2x"} />
                {t("login.microsoft")}
              </Button>
              <Button
                block={true}
                bsStyle={"primary"}
                className={`${style.socialBtn} ${style.bitbucketBtn}`}
                onClick={handleBitbucketLogin}
              >
                <FontAwesome name={"bitbucket"} size={"2x"} />
                {t("login.bitbucket")}
              </Button>
            </Row>
          </Col>
        </Row>
      </Grid>
    </div>
  );
};
