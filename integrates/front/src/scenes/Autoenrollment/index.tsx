/* eslint-disable prefer-promise-reject-errors, no-async-promise-executor */
import { Buffer } from "buffer";

import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError, FetchResult } from "@apollo/client";
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

  const [rootMessages, setRootMessages] = useState({
    message: "",
    type: "success",
  });
  const [orgMessages, setOrgMessages] = useState({
    message: "",
    type: "success",
  });

  const { push, replace } = useHistory();
  const goToOrg = useCallback((): void => {
    setOrgMessages({ message: "", type: "success" });
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

  const [successMutation, setSuccessMutation] = useState({
    group: false,
    organization: false,
    repository: false,
  });

  const setSuccessValues = useCallback(
    (groupValue: boolean, orgValue: boolean, repoValue: boolean): void => {
      setSuccessMutation({
        group: groupValue,
        organization: orgValue,
        repository: repoValue,
      });
    },
    [setSuccessMutation]
  );

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showSubmitAlert, setShowSubmitAlert] = useState(false);

  const [addOrganization] = useMutation<IAddOrganizationResult>(
    ADD_ORGANIZATION,
    {
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
    }
  );

  const [addGroup] = useMutation(ADD_GROUP_MUTATION, {
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
  });

  const [addGitRoot] = useMutation(ADD_GIT_ROOT, {
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

  const timeoutPromise = useCallback(
    async (
      fn: Promise<FetchResult<IAddOrganizationResult>>,
      timeout: number
    ): Promise<unknown> => {
      return new Promise(async (resolve, reject): Promise<void> => {
        setTimeout((): void => {
          reject("API_TIMEOUT");
        }, timeout);
        const response = await fn;
        if (response.data === null || response.data === undefined) {
          reject("ERROR");
        } else {
          resolve(response.data);
        }
      });
    },
    []
  );

  const handleSubmit = useCallback(
    async (values: {
      groupDescription: string;
      groupName: string;
      organizationName: string;
      reportLanguage: string;
      terms: string[];
    }): Promise<void> => {
      setIsSubmitting(true);
      setOrgMessages({
        message: "",
        type: "success",
      });
      setIsRepository(false);
      setOrganization(values);
      async function successOrg(): Promise<boolean> {
        try {
          mixpanel.track("AddOrganization");
          const response = await timeoutPromise(
            addOrganization({
              variables: { name: values.organizationName.toUpperCase() },
            }),
            5000
          );
          const orgResult = response as {
            addOrganization: { success: boolean };
          };
          setSuccessValues(
            successMutation.group,
            orgResult.addOrganization.success,
            successMutation.repository
          );

          return orgResult.addOrganization.success;
        } catch {
          return false;
        }
      }
      if (successMutation.organization ? true : await successOrg()) {
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
        if (successMutation.group || groupSuccess) {
          setSuccessValues(true, true, successMutation.repository);
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
            setSuccessValues(true, true, true);
          } else {
            setForm("repository");
            push("/autoenrollment/repository");
            setRootMessages({
              message: t(
                "autoenrollment.addOrganization.messages.error.repository"
              ),
              type: "error",
            });
          }
        } else {
          setOrgMessages({
            message: t("autoenrollment.addOrganization.messages.error.group"),
            type: "error",
          });
        }
      } else {
        setOrgMessages({
          message: t(
            "autoenrollment.addOrganization.messages.error.organization"
          ),
          type: "error",
        });
      }
      setIsSubmitting(false);
      setShowSubmitAlert(false);
    },
    [
      addGitRoot,
      addGroup,
      addOrganization,
      push,
      replace,
      repository,
      setIsRepository,
      setOrganization,
      setSuccessValues,
      successMutation,
      t,
      timeoutPromise,
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
                    <Col large={"40"} medium={"60"} small={"90"}>
                      <FormContent>
                        <AddOrganization
                          isSubmitting={isSubmitting}
                          onSubmit={handleSubmit}
                          orgMessages={orgMessages}
                          orgValues={organization}
                          setShowSubmitAlert={setShowSubmitAlert}
                          showSubmitAlert={showSubmitAlert}
                          successMutation={successMutation}
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
                    <Col large={"40"} medium={"60"} small={"90"}>
                      <FormContent>
                        <AddRoot
                          initialValues={repository}
                          onCompleted={goToOrg}
                          rootMessages={rootMessages}
                          setForm={setForm}
                          setRepositoryValues={setRepository}
                          setRootMessages={setRootMessages}
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
