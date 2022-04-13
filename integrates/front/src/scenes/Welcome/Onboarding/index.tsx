import React from "react";
import { useTranslation } from "react-i18next";
import { Redirect, Route, Switch } from "react-router-dom";

import { Container } from "./styles";

import { Card, CardBody, CardHeader } from "components/Card";
import { Col, Row } from "components/Layout";

interface IOnboardingProps {
  goToDemo: () => void;
  goToTour: () => void;
}

const Onboarding: React.FC<IOnboardingProps> = ({
  goToDemo,
  goToTour,
}: IOnboardingProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <Container>
      <Switch>
        <Route exact={true} path={"/welcome"}>
          <Row>
            <Col>
              <Row justify={"center"}>
                <Col>
                  <h1>{t("welcome.title")}</h1>
                  <h2>{t("welcome.subtitle")}</h2>
                </Col>
              </Row>
              <Row justify={"center"}>
                <Col large={"30"} medium={"30"} small={"30"}>
                  <Card onClick={goToTour}>
                    <CardHeader>{t("welcome.tour.title")}</CardHeader>
                    <CardBody>
                      <p>{t("welcome.tour.description")}</p>
                    </CardBody>
                  </Card>
                </Col>
                <Col large={"30"} medium={"30"} small={"30"}>
                  <Card onClick={goToDemo}>
                    <CardHeader>{t("welcome.demo.title")}</CardHeader>
                    <CardBody>
                      <p>{t("welcome.demo.description")}</p>
                    </CardBody>
                  </Card>
                </Col>
              </Row>
            </Col>
          </Row>
        </Route>
        <Route exact={true} path={"/welcome/tour"}>
          <p>{"Work in progress"}</p>
        </Route>
        <Redirect to={"/welcome"} />
      </Switch>
    </Container>
  );
};

export { Onboarding };
