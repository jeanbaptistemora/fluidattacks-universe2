import { useQuery } from "@apollo/client";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { Redirect, Route, Switch, useHistory } from "react-router-dom";

import { GET_USER_WELCOME } from "./queries";
import { Container } from "./styles";
import { Tour } from "./Tour";
import type { IGetUserWelcomeResult } from "./types";

import { Card, CardBody, CardHeader } from "components/Card";
import { Col, Row } from "components/Layout";
import { Dashboard } from "scenes/Dashboard";

const Welcome: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  const [browsingDemo, setBrowsingDemo] = useState(false);
  const goToDemo = useCallback((): void => {
    setBrowsingDemo(true);
  }, []);

  const { push } = useHistory();
  const goToTour = useCallback((): void => {
    push("/welcome/tour");
  }, [push]);

  const { data, loading } = useQuery<IGetUserWelcomeResult>(GET_USER_WELCOME);

  if (loading) {
    return <div />;
  }

  const organizations = data === undefined ? [] : data.me.organizations;
  const isFirstTimeUser =
    organizations.length === 1 &&
    organizations[0].name.toLowerCase() === "imamura";

  if (isFirstTimeUser && !browsingDemo) {
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
            <Tour />
          </Route>
          <Redirect to={"/welcome"} />
        </Switch>
      </Container>
    );
  }

  return <Dashboard />;
};

export { Welcome };
