import React from "react";
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
  return (
    <Container>
      <Switch>
        <Route exact={true} path={"/welcome"}>
          <Row>
            <Col>
              <Row justify={"center"}>
                <Col>
                  <h1>{"Welcome to ASM"}</h1>
                  <h2>{"Let's get started"}</h2>
                </Col>
              </Row>
              <Row justify={"center"}>
                <Col large={"30"} medium={"30"} small={"30"}>
                  <Card onClick={goToTour}>
                    <CardHeader>{"Platform tour"}</CardHeader>
                    <CardBody>
                      <p>
                        {"Take our interactive tour to get familiar with ASM"}
                      </p>
                    </CardBody>
                  </Card>
                </Col>
                <Col large={"30"} medium={"30"} small={"30"}>
                  <Card onClick={goToDemo}>
                    <CardHeader>{"Browse demo"}</CardHeader>
                    <CardBody>
                      <p>{"See ASM in action inside an interactive demo."}</p>
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
