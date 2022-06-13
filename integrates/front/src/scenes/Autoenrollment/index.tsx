/* eslint-disable prefer-promise-reject-errors, no-async-promise-executor */
import { Buffer } from "buffer";

import { useMutation } from "@apollo/client";
import type { ApolloError, FetchResult } from "@apollo/client";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import Lottie from "react-lottie-player";
import { Redirect, Route, Switch, useHistory } from "react-router-dom";

import { AddOrganization } from "./components/AddOrganization";
import { AddRoot } from "./components/AddRoot";
import { Sidebar } from "./components/Sidebar";
import { Container, DashboardContent, FormContent } from "./styles";

import { Col, Row } from "components/Layout";
import scan from "resources/scan.json";
import {
  handleGroupCreateError,
  handleRootCreateError,
} from "scenes/Autoenrollment/helpers";
import {
  ADD_GIT_ROOT,
  ADD_GROUP_MUTATION,
  ADD_ORGANIZATION,
} from "scenes/Autoenrollment/queries";
import type {
  IAddOrganizationResult,
  IOrgAttr,
  IRootAttr,
} from "scenes/Autoenrollment/types";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IAutoenrollmentProps {
  group?: string;
  organization?: string;
}

const Autoenrollment: React.FC<IAutoenrollmentProps> = (
  props: Readonly<IAutoenrollmentProps>
): JSX.Element => {
  const { group = "", organization = "" } = props;
  const { t } = useTranslation();

  useEffect((): void => {
    mixpanel.track("AutoenrollmentWelcome");
  }, []);

  const [rootMessages, setRootMessages] = useState({
    message: "",
    type: "success",
  });
  const [orgMessages, setOrgMessages] = useState({
    message: "",
    type: "success",
  });

  const { push } = useHistory();
  const goToOrg = useCallback((): void => {
    setOrgMessages({ message: "", type: "success" });
    push("/autoenrollment/organization");
  }, [push]);

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

  const [organizationValues, setOrganizationValues] = useState<IOrgAttr>({
    groupDescription: "",
    groupName: group,
    organizationName: organization,
    reportLanguage: "",
    terms: [],
  });

  const [successMutation, setSuccessMutation] = useState({
    group: group !== "",
    organization: organization !== "",
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
      setShowSubmitAlert(false);
      setOrganizationValues(values);
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
        const groupResult = successMutation.group
          ? { data: undefined }
          : await addGroup({
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
            setSuccessValues(true, true, true);
            mixpanel.track("AutoenrollSubmit", {
              addGroup: true,
              addOrg: true,
              addRoot: true,
              group: values.groupName.toLowerCase(),
              organization: values.organizationName.toLowerCase(),
              url: url.trim(),
            });
            location.replace(
              `/orgs/${values.organizationName.toLowerCase()}/groups/${values.groupName.toLowerCase()}/scope`
            );
          } else {
            mixpanel.track("AutoenrollSubmit", {
              addGroup: true,
              addOrg: true,
              addRoot: false,
              group: values.groupName.toLowerCase(),
              organization: values.organizationName.toLowerCase(),
              url: url.trim(),
            });
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
          mixpanel.track("AutoenrollSubmit", {
            addGroup: false,
            addOrg: true,
            addRoot: false,
            group: values.groupName.toLowerCase(),
            organization: values.organizationName.toLowerCase(),
            url: url.trim(),
          });
        }
      } else {
        setOrgMessages({
          message: t(
            "autoenrollment.addOrganization.messages.error.organization"
          ),
          type: "error",
        });
        mixpanel.track("AutoenrollSubmit", {
          addGroup: false,
          addOrg: false,
          addRoot: false,
          group: values.groupName.toLowerCase(),
          organization: values.organizationName.toLowerCase(),
          url: repository.url.trim(),
        });
      }
      setIsSubmitting(false);
    },
    [
      addGitRoot,
      addGroup,
      addOrganization,
      push,
      repository,
      setOrganizationValues,
      setSuccessValues,
      successMutation,
      t,
      timeoutPromise,
    ]
  );

  return (
    <Container>
      <React.Fragment>
        <Sidebar />
        <DashboardContent id={"dashboard"}>
          <Switch>
            <Route exact={true} path={"/autoenrollment/organization"}>
              <Col large={"100"} medium={"100"} small={"100"}>
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
                        orgValues={organizationValues}
                        setShowSubmitAlert={setShowSubmitAlert}
                        showSubmitAlert={showSubmitAlert}
                        successMutation={successMutation}
                      />
                    </FormContent>
                  </Col>
                </Row>
              </Col>
            </Route>
            <Route exact={true} path={"/autoenrollment/repository"}>
              <Col large={"100"} medium={"100"} small={"100"}>
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
                        setRepositoryValues={setRepository}
                        setRootMessages={setRootMessages}
                      />
                    </FormContent>
                  </Col>
                </Row>
              </Col>
            </Route>
            <Route exact={true} path={"/autoenrollment/standby"}>
              <Col large={"100"} medium={"100"} small={"100"}>
                <Row justify={"center"}>
                  <Col large={"30"} medium={"50"} small={"70"}>
                    <FormContent>
                      <Row align={"center"} justify={"center"}>
                        <Col>
                          <Lottie
                            animationData={scan}
                            play={true}
                            // eslint-disable-next-line react/forbid-component-props
                            style={{ height: 150, margin: "auto", width: 150 }}
                          />
                        </Col>
                      </Row>
                      <Row justify={"center"}>
                        <Col>
                          <h2>{t("autoenrollment.standby.title")}</h2>
                          <p>{t("autoenrollment.standby.subtitle")}</p>
                        </Col>
                      </Row>
                    </FormContent>
                  </Col>
                </Row>
              </Col>
            </Route>
            <Redirect to={"/autoenrollment/repository"} />
          </Switch>
        </DashboardContent>
      </React.Fragment>
    </Container>
  );
};

export { Autoenrollment };
