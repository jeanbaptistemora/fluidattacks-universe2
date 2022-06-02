import { useQuery } from "@apollo/client";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { Redirect, Route, Switch, useHistory } from "react-router-dom";

import { AddOrganization } from "./components/AddOrganization";
import { AddRoot } from "./components/AddRoot";
import { Sidebar } from "./components/Sidebar";
import { GET_USER_WELCOME } from "./queries";
import { Container, DashboardContent, FormContent } from "./styles";
import type { IGetUserWelcomeResult, IOrgAttr, IRootAttr } from "./types";

import { Col, Row } from "components/Layout";
import { Dashboard } from "scenes/Dashboard";
import { Logger } from "utils/logger";

const Autoenrollment: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  const { push } = useHistory();
  const goToOrg = useCallback((): void => {
    push("/autoenrollment/organization");
  }, [push]);

  const [form, setForm] = useState("repository");
  const [isRepository, setIsRepository] = useState(false);
  const [repository, setRepository] = useState<IRootAttr>({
    branch: "",
    credentials: {
      auth: "TOKEN",
      id: "",
      key: "",
      name: "",
      password: "",
      token: "",
      type: "",
      user: "",
    },
    env: "",
    exclusions: [],
    url: "",
  });

  const [organization, setOrganization] = useState<IOrgAttr>({
    groupDescription: "",
    groupName: "",
    organizationName: "",
    reportLanguage: "",
    terms: [],
  });

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
  const isFirstTimeUser =
    organizations.length === 0 ||
    (organizations.length === 1 && organizations[0].name === "okada");

  if (isFirstTimeUser || !isRepository) {
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
                        <AddOrganization
                          orgValues={organization}
                          repositoryValues={repository}
                          setForm={setForm}
                          setIsRepository={setIsRepository}
                          setOrgValues={setOrganization}
                        />
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
                        <AddRoot
                          initialValues={repository}
                          onCompleted={goToOrg}
                          setForm={setForm}
                          setRepositoryValues={setRepository}
                        />
                      </FormContent>
                    </Col>
                  </Row>
                </Col>
              </Row>
            </Route>
            {form === "repository" && (
              <Redirect to={"/autoenrollment/repository"} />
            )}
            {form === "organization" && (
              <Redirect to={"/autoenrollment/organization"} />
            )}
          </Switch>
        </DashboardContent>
      </Container>
    );
  }

  return <Dashboard />;
};

export { Autoenrollment };
