import { useQuery } from "@apollo/client";
import React from "react";
import { useTranslation } from "react-i18next";
import { Redirect, Route, Switch } from "react-router-dom";

import { AddOrganization } from "./components/AddOrganization";
import { GET_USER_WELCOME } from "./queries";
import { Container, DashboardContent } from "./styles";
import type { IGetUserWelcomeResult } from "./types";

import { Card, CardBody } from "components/Card";
import { Col, Row } from "components/Layout";
import { Sidebar } from "scenes/Autoenrollment/components/Sidebar";
import { Dashboard } from "scenes/Dashboard";
import { Logger } from "utils/logger";

const Autoenrollment: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  const { data, loading } = useQuery<IGetUserWelcomeResult>(GET_USER_WELCOME, {
    onError: (error): void => {
      error.graphQLErrors.forEach(({ message }): void => {
        Logger.error("An error occurred loading user welcome", message);
      });
    },
  });

  if (loading) {
    return <div />;
  }

  const organizations = data === undefined ? [] : data.me.organizations;
  const isFirstTimeUser = organizations.length === 0;

  if (isFirstTimeUser) {
    return (
      <Container>
        <Sidebar />
        <DashboardContent id={"dashboard"}>
          <Switch>
            <Route exact={true} path={"/autoenrollment/tour"}>
              <Row align={"center"} justify={"center"}>
                <Col>
                  <Row justify={"center"}>
                    <Col>
                      <h2>{t("autoenrollment.addGroup.title")}</h2>
                      <p>{t("autoenrollment.addGroup.subtitle")}</p>
                    </Col>
                  </Row>
                  <Row justify={"center"}>
                    <Col large={"60"} medium={"80"} small={"90"}>
                      <Card>
                        <CardBody>
                          <AddOrganization />
                        </CardBody>
                      </Card>
                    </Col>
                  </Row>
                </Col>
              </Row>
            </Route>
            <Redirect to={"/autoenrollment/tour"} />
          </Switch>
        </DashboardContent>
      </Container>
    );
  }

  return <Dashboard />;
};

export { Autoenrollment };
