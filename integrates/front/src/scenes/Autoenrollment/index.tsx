import { Buffer } from "buffer";

import { useMutation, useQuery } from "@apollo/client";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { Fragment, useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { AddOrganization } from "./components/AddOrganization";
import { AddRoot } from "./components/AddRoot";
import { LanguagesButton } from "./components/LanguagesButton";
import { Sidebar } from "./components/Sidebar";
import { Standby } from "./components/Standby";
import { ContainerAutoenrollment, DashboardContent } from "./styles";
import { isPersonalEmail } from "./utils";

import { Announce } from "components/Announce";
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
  ADD_GROUP,
  ADD_ORGANIZATION,
  GET_STAKEHOLDER_GROUPS,
} from "scenes/Autoenrollment/queries";
import type {
  IAddGitRootResult,
  IAddGroupResult,
  IAddOrganizationResult,
  IGetStakeholderGroupsResult,
  IOrgAttr,
  IRootAttr,
} from "scenes/Autoenrollment/types";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

type TEnrollPages = "organization" | "repository" | "standBy";

const Autoenrollment: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  // State management
  const [page, setPage] = useState<TEnrollPages>("repository");
  const [rootMessages, setRootMessages] = useState({
    message: "",
    type: "success",
  });
  const [orgMessages, setOrgMessages] = useState({
    message: "",
    type: "success",
  });

  const [redirectPath, setRedirectPath] = useState("/logout");

  const [repository, setRepository] = useState<IRootAttr>({
    branch: "",
    credentials: {
      auth: "TOKEN",
      azureOrganization: undefined,
      isPat: false,
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
    organizationCountry: "",
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

  const [showSubmitAlert, setShowSubmitAlert] = useState(false);

  // API operations
  const { data } = useQuery<IGetStakeholderGroupsResult>(
    GET_STAKEHOLDER_GROUPS,
    {
      onCompleted: async ({ me }): Promise<void> => {
        const organizationCountry = me.organizations[0]?.country || "";
        const organizationName = me.organizations[0]?.name || "";
        const group = me.organizations[0]?.groups[0]?.name || "";

        setOrganizationValues({
          ...organizationValues,
          groupName: group,
          organizationCountry,
          organizationName,
        });
        setSuccessMutation({
          group: group !== "",
          organization: organizationName !== "",
          repository: false,
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

  const [addOrganization] = useMutation<IAddOrganizationResult>(
    ADD_ORGANIZATION,
    {
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

  const [addGroup] = useMutation<IAddGroupResult>(ADD_GROUP, {
    onCompleted: (result): void => {
      if (result.addGroup.success) {
        msgSuccess(
          t("organization.tabs.groups.newGroup.success"),
          t("organization.tabs.groups.newGroup.titleSuccess")
        );
      }
    },
    onError: (error): void => {
      handleGroupCreateError(error.graphQLErrors, setOrgMessages);
    },
  });

  const [addGitRoot] = useMutation<IAddGitRootResult>(ADD_GIT_ROOT, {
    onCompleted: (result): void => {
      if (result.addGitRoot.success) {
        msgSuccess(
          t("autoenrollment.messages.success.body"),
          t("autoenrollment.messages.success.title")
        );
      }
    },
    onError: (error): void => {
      handleRootCreateError(error.graphQLErrors, setOrgMessages);
      setShowSubmitAlert(false);
    },
  });

  const [addEnrollment] = useMutation(ADD_ENROLLMENT, {
    onError: (error): void => {
      handleEnrollmentCreateError(error.graphQLErrors, setOrgMessages);
    },
  });

  // Callbacks
  const goToOrg = useCallback((): void => {
    setOrgMessages({ message: "", type: "success" });
    setPage("organization");
  }, [setPage]);

  const handleSubmit = useCallback(
    async (values: {
      groupDescription: string;
      groupName: string;
      organizationCountry: string;
      organizationName: string;
      reportLanguage: string;
      terms: string[];
    }): Promise<void> => {
      setOrgMessages({
        message: "",
        type: "success",
      });
      setShowSubmitAlert(false);
      setOrganizationValues(values);

      async function addNewOrganization(): Promise<boolean> {
        try {
          mixpanel.track("AddOrganization");
          const response = await addOrganization({
            variables: {
              country: values.organizationCountry,
              name: values.organizationName.toUpperCase(),
            },
          });
          const orgResult = response.data;

          return orgResult ? orgResult.addOrganization.success : false;
        } catch {
          return false;
        }
      }

      async function addNewGroup(): Promise<boolean> {
        try {
          mixpanel.track("AddGroup");
          const response = await addGroup({
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
          const groupResult = response.data;

          return groupResult ? groupResult.addGroup.success : false;
        } catch {
          return false;
        }
      }

      async function addNewRoot(): Promise<boolean> {
        try {
          const { branch, credentials, env, exclusions, url } = repository;

          mixpanel.track("AddGitRoot");
          const response = await addGitRoot({
            variables: {
              branch: branch.trim(),
              credentials:
                credentials.key === "" &&
                credentials.user === "" &&
                credentials.password === "" &&
                credentials.token === ""
                  ? null
                  : {
                      azureOrganization:
                        _.isUndefined(credentials.azureOrganization) ||
                        _.isUndefined(credentials.isPat) ||
                        !credentials.isPat
                          ? undefined
                          : credentials.azureOrganization,
                      isPat: _.isUndefined(credentials.isPat)
                        ? false
                        : credentials.isPat,
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
          const rootResult = response.data;

          return rootResult ? rootResult.addGitRoot.success : false;
        } catch {
          return false;
        }
      }

      if (successMutation.organization ? true : await addNewOrganization()) {
        if (successMutation.group ? true : await addNewGroup()) {
          if (await addNewRoot()) {
            localStorage.clear();
            sessionStorage.clear();
            await addEnrollment();
            setRedirectPath(
              `/orgs/${values.organizationName.toLowerCase()}/groups/${values.groupName.toLowerCase()}/scope`
            );
            setPage("standBy");
          } else {
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
    },
    [
      addEnrollment,
      addGitRoot,
      addGroup,
      addOrganization,
      repository,
      setRedirectPath,
      setOrganizationValues,
      setPage,
      successMutation,
      t,
    ]
  );

  function redirect(): void {
    /*
     * Intentional full page reload as we're in a conditionally rendered view
     * No way to use the router to get to the dashboard from here
     */
    location.replace(redirectPath);
  }

  if (data === undefined || hasPersonalEmail === undefined) {
    return <div />;
  }

  const { trial } = data.me.company;

  if (trial.startDate) {
    return <Announce message={t("autoenrollment.companyAlreadyInTrial")} />;
  }

  if (hasPersonalEmail) {
    return <Announce message={t("autoenrollment.corporateOnly")} />;
  }

  const pages: Record<TEnrollPages, JSX.Element> = {
    organization: (
      <Fragment>
        <Text bright={0} mb={1} mt={5} ta={"center"} tone={"red"}>
          {t("autoenrollment.step2")}
        </Text>
        <Text fw={7} mb={1} size={"medium"} ta={"center"}>
          {t("autoenrollment.setupOrganization")}
        </Text>
        <Text mb={4} ta={"center"}>
          {t("autoenrollment.aboutToStart")}
        </Text>
        <Row justify={"center"}>
          <Col lg={40} md={60} sm={90}>
            <Card>
              <AddOrganization
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
        <Text bright={0} mb={3} mt={5} ta={"center"} tone={"red"}>
          {t("autoenrollment.step1")}
        </Text>
        <Text fw={7} mb={2} size={"medium"} ta={"center"}>
          {t("autoenrollment.addRepository")}
        </Text>
        <Text ta={"center"}>{t("autoenrollment.canAddMore")}</Text>
        <LanguagesButton />
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
            <Standby onClose={redirect}>
              <Text fw={7} mb={2} size={"medium"} ta={"center"}>
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
    <ContainerAutoenrollment>
      <Sidebar />
      <DashboardContent id={"dashboard"}>{pages[page]}</DashboardContent>
    </ContainerAutoenrollment>
  );
};

export { Autoenrollment };
