import { Buffer } from "buffer";

import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { Redirect, Route, Switch, useHistory } from "react-router-dom";

import { AddOrganization } from "./components/AddOrganization";
import { AddRoot } from "./components/AddRoot";
import { Sidebar } from "./components/Sidebar";
import { Container, DashboardContent, FormContent } from "./styles";

import { Col, Row } from "components/Layout";
import {
  handleGroupCreateError,
  handleRootCreateError,
} from "scenes/Autoenrollment/helpers";
import {
  ADD_GIT_ROOT,
  ADD_GROUP_MUTATION,
  ADD_ORGANIZATION,
  GET_USER_WELCOME,
} from "scenes/Autoenrollment/queries";
import type {
  IAddOrganizationResult,
  IGetUserWelcomeResult,
  IOrgAttr,
  IRootAttr,
} from "scenes/Autoenrollment/types";
import { Dashboard } from "scenes/Dashboard";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const Autoenrollment: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  const { push, replace } = useHistory();
  const goToOrg = useCallback((): void => {
    push("/autoenrollment/organization");
  }, [push]);

  const [form, setForm] = useState("repository");
  const [isRepository, setIsRepository] = useState(true);
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

  const [orgMessages, setOrgMessages] = useState({
    message: "",
    type: "success",
  });

  const [showSubmitAlert, setShowSubmitAlert] = useState(false);

  const [addOrganization, { loading: submittingOrg }] =
    useMutation<IAddOrganizationResult>(ADD_ORGANIZATION, {
      awaitRefetchQueries: true,
      onCompleted: (result): void => {
        if (result.addOrganization.success) {
          mixpanel.track("NewOrganization", {
            OrganizationId: result.addOrganization.organization.id,
            OrganizationName: result.addOrganization.organization.name,
          });
        }
      },
      onError: (error): void => {
        error.graphQLErrors.forEach(({ message }): void => {
          if (message === "Access denied") {
            msgError(t("sidebar.newOrganization.modal.invalidName"));
          } else {
            Logger.error(
              "An error occurred creating new organization",
              message
            );
          }
        });
      },
      refetchQueries: [GET_USER_WELCOME],
    });

  const [addGroup, { loading: submittingGroup }] = useMutation(
    ADD_GROUP_MUTATION,
    {
      onCompleted: (result: { addGroup: { success: boolean } }): void => {
        if (result.addGroup.success) {
          msgSuccess(
            t("organization.tabs.groups.newGroup.success"),
            t("organization.tabs.groups.newGroup.titleSuccess")
          );
        }
      },
      onError: ({ graphQLErrors }: ApolloError): void => {
        handleGroupCreateError(graphQLErrors, setOrgMessages);
      },
    }
  );

  const [addGitRoot, { loading: submittingRoot }] = useMutation(ADD_GIT_ROOT, {
    onCompleted: (result: { addGitRoot: { success: boolean } }): void => {
      if (result.addGitRoot.success) {
        msgSuccess(
          t("autoenrollment.addOrganization.messages.success.body"),
          t("autoenrollment.addOrganization.messages.success.title")
        );
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      handleRootCreateError(graphQLErrors, setOrgMessages);
      setShowSubmitAlert(false);
    },
  });

  const handleSubmit = useCallback(
    async (values: {
      groupDescription: string;
      groupName: string;
      organizationName: string;
      reportLanguage: string;
      terms: string[];
    }): Promise<void> => {
      setOrgMessages({
        message: "",
        type: "success",
      });
      setIsRepository(false);
      setShowSubmitAlert(false);
      setOrganization(values);
      mixpanel.track("AddOrganization");
      const orgResult = await addOrganization({
        variables: { name: values.organizationName.toUpperCase() },
      });
      const orgSuccess =
        orgResult.data === null || orgResult.data === undefined
          ? false
          : orgResult.data.addOrganization.success;
      if (orgSuccess) {
        mixpanel.track("AddGroup");
        const groupResult = await addGroup({
          variables: {
            description: values.groupDescription,
            groupName: values.groupName.toUpperCase(),
            hasMachine: true,
            hasSquad: false,
            language: values.reportLanguage,
            organizationName: values.organizationName,
            service: "WHITE",
            subscription: "CONTINUOUS",
          },
        });
        const { branch, credentials, env, exclusions, url } = repository;
        const groupSuccess =
          groupResult.data === null || groupResult.data === undefined
            ? false
            : groupResult.data.addGroup.success;
        if (groupSuccess) {
          mixpanel.track("AddGitRoot");
          const rootResult = await addGitRoot({
            variables: {
              branch: branch.trim(),
              credentials:
                credentials.key === "" &&
                credentials.user === "" &&
                credentials.password === "" &&
                credentials.id === "" &&
                credentials.token === ""
                  ? null
                  : {
                      id: credentials.id,
                      key:
                        credentials.key === ""
                          ? undefined
                          : Buffer.from(credentials.key).toString("base64"),
                      name: credentials.name,
                      password: credentials.password,
                      token: credentials.token,
                      type: credentials.type,
                      user: credentials.user,
                    },
              environment: env,
              gitignore: exclusions,
              groupName: values.groupName.toUpperCase(),
              includesHealthCheck: false,
              nickname: "",
              url: url.trim(),
              useVpn: false,
            },
          });
          const rootSuccess =
            rootResult.data === null || rootResult.data === undefined
              ? false
              : rootResult.data.addGitRoot.success;
          if (rootSuccess) {
            localStorage.clear();
            sessionStorage.clear();
            replace(
              `/orgs/${values.organizationName.toLowerCase()}/groups/${values.groupName.toLowerCase()}/scope`
            );
            setIsRepository(true);
          } else {
            setIsRepository(false);
            setOrgMessages({
              message: "Invalid repository info, please change your inputs",
              type: "error",
            });
          }
        } else {
          setOrgMessages({
            message: "Invalid or used Group Name, please change your input",
            type: "error",
          });
        }
      } else {
        setOrgMessages({
          message:
            "Invalid or used Organization Name, please change your input",
          type: "error",
        });
      }
      setShowSubmitAlert(false);
    },
    [
      addGitRoot,
      addGroup,
      addOrganization,
      replace,
      repository,
      setIsRepository,
      setOrganization,
    ]
  );

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
                          isSubmitting={
                            submittingOrg || submittingGroup || submittingRoot
                          }
                          onSubmit={handleSubmit}
                          orgMessages={orgMessages}
                          orgValues={organization}
                          setShowSubmitAlert={setShowSubmitAlert}
                          showSubmitAlert={showSubmitAlert}
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
