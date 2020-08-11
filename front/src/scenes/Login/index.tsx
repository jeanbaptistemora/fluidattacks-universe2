import mixpanel from "mixpanel-browser";
import React from "react";
import { Button, Col, Grid, Row } from "react-bootstrap";
import FontAwesome from "react-fontawesome";
import { Slide, toast } from "react-toastify";

import { useTranslation } from "react-i18next";
import { default as logo } from "../../resources/integrates.svg";
import { default as style } from "./index.css";

const login: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  // Side effects
  const onMount: (() => void) = (): void => {
    toast.info(
      <div>
        <p>{t("login.2fa")}</p>
        <div>
          <Col xs={12} md={6}>
            <Button
              href="http://bit.ly/2Gpjt6h"
              bsStyle="danger"
              block={true}
            >
              <FontAwesome name="google" size="2x" />&nbsp;
            </Button>
          </Col>
          <Col xs={12} md={6}>
            <Button
              href="http://bit.ly/2Gp1L2X"
              bsStyle="primary"
              block={true}
            >
              <FontAwesome name="windows" size="2x" />&nbsp;
            </Button>
          </Col>
        </div>
      </div>,
      { autoClose: false, className: style.twofactor, transition: Slide },
    );
  };
  React.useEffect(onMount, []);

  // Event handlers
  const handleGoogleLogin: (() => void) = (): void => {
    mixpanel.track("Login Google");
    window.location.href = "/integrates/oauth/login/google-oauth2/";
  };

  const handleMicrosoftLogin: (() => void) = (): void => {
    mixpanel.track("Login Azure");
    window.location.href = "/integrates/oauth/login/azuread-tenant-oauth2/";
  };

  return (
    <div className={style.container}>
      <Grid>
        <Row className={style.content}>
          <Col md={4} mdOffset={4}>
            <Row><img src={logo} alt="logo" /></Row>
            <Row className="text-center">
              <p>{t("login.auth")}</p>
              <p>{t("login.newuser")}</p>
            </Row>
            <Row>
              <Button
                bsStyle="danger"
                className={style.googleBtn}
                onClick={handleGoogleLogin}
                block={true}
              >
                <FontAwesome name="google" size="2x" />
                {t("login.google")}
              </Button>
              <Button
                bsStyle="primary"
                className={style.microsoftBtn}
                onClick={handleMicrosoftLogin}
                block={true}
              >
                <FontAwesome name="windows" size="2x" />
                {t("login.microsoft")}
              </Button>
            </Row>
          </Col>
        </Row>
      </Grid>
    </div>
  );
};

export { login as Login };
