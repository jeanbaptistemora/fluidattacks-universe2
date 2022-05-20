import { useQuery } from "@apollo/client";
import React from "react";
import { useTranslation } from "react-i18next";
import { Redirect, Route, Switch } from "react-router-dom";

import { AddOrganization } from "./components/AddOrganization";
import { AddRoot } from "./components/AddRoot";
import { Sidebar } from "./components/Sidebar";
import { GET_USER_WELCOME } from "./queries";
import { Container, DashboardContent, FormContent } from "./styles";
import type { IGetUserWelcomeResult } from "./types";

import { Col, Row } from "components/Layout";
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
            <Route exact={true} path={"/autoenrollment/organization"}>
              <Row align={"center"} justify={"center"}>
                <Col>
                  <Row justify={"center"}>
                    <Col>
                      <h2>{t("autoenrollment.addOrganization.title")}</h2>
                    </Col>
                  </Row>
                  <Row justify={"center"}>
                    <Col large={"25"} medium={"50"} small={"70"}>
                      <FormContent>
                        <AddOrganization />
                      </FormContent>
                    </Col>
                  </Row>
                </Col>
              </Row>
            </Route>
            <Route exact={true} path={"/autoenrollment/repository"}>
              <Row align={"center"} justify={"center"}>
                <Col>
                  <Row justify={"center"}>
                    <Col>
                      <h2>{t("autoenrollment.addRoot.title")}</h2>
                      <p>{t("autoenrollment.addRoot.subtitle")}</p>
                    </Col>
                  </Row>
                  <Row justify={"center"}>
                    <Col large={"40"} medium={"60"} small={"80"}>
                      <FormContent>
                        <AddRoot />
                      </FormContent>
                    </Col>
                  </Row>
                </Col>
              </Row>
            </Route>
            <Redirect to={"/autoenrollment/repository"} />
          </Switch>
        </DashboardContent>
      </Container>
    );
  }

  return <Dashboard />;
};

export { Autoenrollment };
