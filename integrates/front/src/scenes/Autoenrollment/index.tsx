/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable prefer-promise-reject-errors, no-async-promise-executor */
import { Buffer } from "buffer";

import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError, FetchResult } from "@apollo/client";
import { faMessage } from "@fortawesome/free-solid-svg-icons";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { Fragment, useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { AddOrganization } from "./components/AddOrganization";
import { AddRoot } from "./components/AddRoot";
import { Sidebar } from "./components/Sidebar";
import { Standby } from "./components/Standby";
import { Container, DashboardContent } from "./styles";
import { isPersonalEmail } from "./utils";

import { Announce } from "components/Announce";
import { Button } from "components/Button";
import { Card } from "components/Card";
import { Col, Row } from "components/Layout";
import { Text } from "components/Text";
import {
  handleEnrollmentCreateError,
  handleGroupCreateError,
  handleRootCreateError,
} from "scenes/Autoenrollment/helpers";
import {
  ADD_ENROLLMENT,
  ADD_GIT_ROOT,
  ADD_GROUP_MUTATION,
  ADD_ORGANIZATION,
  GET_STAKEHOLDER_GROUPS,
} from "scenes/Autoenrollment/queries";
import type {
  IAddOrganizationResult,
  IGetStakeholderGroupsResult,
  IOrgAttr,
  IRootAttr,
} from "scenes/Autoenrollment/types";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { toggleZendesk } from "utils/widgets";

type TEnrollPages = "organization" | "repository" | "standBy";

const Autoenrollment: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  useEffect((): void => {
    mixpanel.track("AutoenrollmentWelcome");
  }, []);

  const [page, setPage] = useState<TEnrollPages>("repository");
  const [rootMessages, setRootMessages] = useState({
    message: "",
    type: "success",
  });
  const [orgMessages, setOrgMessages] = useState({
    message: "",
    type: "success",
  });

  const goToOrg = useCallback((): void => {
    setOrgMessages({ message: "", type: "success" });
    setPage("organization");
  }, [setPage]);

  const [asmLocation, setAsmLocation] = useState("/logout");

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
    groupName: "",
    organizationName: "",
    reportLanguage: "",
    terms: [],
  });

  const [successMutation, setSuccessMutation] = useState({
    group: false,
    organization: false,
    repository: false,
  });

  const [hasPersonalEmail, setHasPersonalEmail] = useState<boolean | undefined>(
    undefined
  );

  const { data } = useQuery<IGetStakeholderGroupsResult>(
    GET_STAKEHOLDER_GROUPS,
    {
      onCompleted: async ({ me }): Promise<void> => {
        const organization = me.organizations[0]?.name || "";
        const group = me.organizations[0]?.groups[0]?.name || "";

        setOrganizationValues({
          ...organizationValues,
          groupName: group,
          organizationName: organization,
        });
        setSuccessMutation({
          ...successMutation,
          group: group !== "",
          organization: organization !== "",
        });
        setHasPersonalEmail(await isPersonalEmail(me.userEmail));
      },
      onError: (error): void => {
        error.graphQLErrors.forEach(({ message }): void => {
          Logger.error("An error occurred loading stakeholder groups", message);
        });
      },
    }
  );

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
          t("autoenrollment.messages.success.body"),
          t("autoenrollment.messages.success.title")
        );
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      handleRootCreateError(graphQLErrors, setOrgMessages);
      setShowSubmitAlert(false);
    },
  });

  const [addEnrollment] = useMutation(ADD_ENROLLMENT, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      handleEnrollmentCreateError(graphQLErrors, setOrgMessages);
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
            await addEnrollment();
            setAsmLocation(
              `/orgs/${values.organizationName.toLowerCase()}/groups/${values.groupName.toLowerCase()}/scope`
            );
            setPage("standBy");
          } else {
            mixpanel.track("AutoenrollSubmit", {
              addGroup: true,
              addOrg: true,
              addRoot: false,
              group: values.groupName.toLowerCase(),
              organization: values.organizationName.toLowerCase(),
              url: url.trim(),
            });
            setPage("repository");
            setRootMessages({
              message: t("autoenrollment.messages.error.repository"),
              type: "error",
            });
          }
        } else {
          setOrgMessages({
            message: t("autoenrollment.messages.error.group"),
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
          message: t("autoenrollment.messages.error.organization"),
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
      addEnrollment,
      addGitRoot,
      addGroup,
      addOrganization,
      repository,
      setAsmLocation,
      setOrganizationValues,
      setPage,
      setSuccessValues,
      successMutation,
      t,
      timeoutPromise,
    ]
  );

  function asmRedirect(): void {
    location.replace(asmLocation);
  }

  if (data === undefined || hasPersonalEmail === undefined) {
    return <div />;
  }

  if (hasPersonalEmail) {
    return <Announce message={t("autoenrollment.corporateOnly")} />;
  }

  toggleZendesk();

  const pages: Record<TEnrollPages, JSX.Element> = {
    organization: (
      <Fragment>
        <Text bright={0} mb={1} mt={5} ta={"center"} tone={"red"}>
          {t("autoenrollment.step2")}
        </Text>
        <Text fw={7} mb={1} size={4} ta={"center"}>
          {t("autoenrollment.setupOrganization")}
        </Text>
        <Text mb={4} ta={"center"}>
          {t("autoenrollment.aboutToStart")}
        </Text>
        <Row justify={"center"}>
          <Col lg={40} md={60} sm={90}>
            <Card>
              <AddOrganization
                isSubmitting={isSubmitting}
                onSubmit={handleSubmit}
                orgMessages={orgMessages}
                orgValues={organizationValues}
                setShowSubmitAlert={setShowSubmitAlert}
                showSubmitAlert={showSubmitAlert}
                successMutation={successMutation}
              />
            </Card>
          </Col>
        </Row>
      </Fragment>
    ),
    repository: (
      <Fragment>
        <Text bright={0} mb={1} mt={5} ta={"center"} tone={"red"}>
          {t("autoenrollment.step1")}
        </Text>
        <Text fw={7} mb={1} size={4} ta={"center"}>
          {t("autoenrollment.addRepository")}
        </Text>
        <Text mb={4} ta={"center"}>
          {t("autoenrollment.canAddMore")}
        </Text>
        <Row justify={"center"}>
          <Col lg={40} md={60} sm={90}>
            <Card>
              <AddRoot
                initialValues={repository}
                onCompleted={goToOrg}
                rootMessages={rootMessages}
                setRepositoryValues={setRepository}
                setRootMessages={setRootMessages}
              />
            </Card>
          </Col>
        </Row>
      </Fragment>
    ),
    standBy: (
      <Row justify={"center"}>
        <div className={"pb4"} />
        <Col lg={30} md={50} sm={70}>
          <Card>
            <Standby onClose={asmRedirect}>
              <Text fw={7} mb={2} size={4} ta={"center"}>
                {t("autoenrollment.standby.title")}
              </Text>
              <Text ta={"center"}>{t("autoenrollment.standby.subtitle")}</Text>
            </Standby>
          </Card>
        </Col>
      </Row>
    ),
  };

  return (
    <Container>
      <Sidebar />
      <DashboardContent id={"dashboard"}>
        {pages[page]}
        <div className={"absolute bottom-0 ma3 right-0"}>
          <Button icon={faMessage} onClick={toggleZendesk} variant={"primary"}>
            {"Chat"}
          </Button>
        </div>
      </DashboardContent>
    </Container>
  );
};

export { Autoenrollment };
