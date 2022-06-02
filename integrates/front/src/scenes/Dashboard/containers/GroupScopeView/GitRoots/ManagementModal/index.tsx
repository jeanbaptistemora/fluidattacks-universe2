import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import React from "react";
import { useTranslation } from "react-i18next";
import { MemoryRouter, Route, Switch } from "react-router-dom";

import { Environments } from "./environments";
import { Repository } from "./repository";

import { Secrets } from "../../Secrets";
import type { IGitRootAttr } from "../../types";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Modal } from "components/Modal";
import { Tab, Tabs } from "components/Tabs";
import { TabContent } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";

interface IManagementModalProps {
  groupName: string;
  initialValues: IGitRootAttr | undefined;
  modalMessages: { message: string; type: string };
  nicknames: string[];
  onClose: () => void;
  onSubmitEnvs: (values: IGitRootAttr) => Promise<void>;
  onSubmitRepo: (values: IGitRootAttr) => Promise<void>;
  runTour: boolean;
  finishTour: () => void;
}

const ManagementModal: React.FC<IManagementModalProps> = ({
  groupName,
  initialValues = {
    __typename: "GitRoot",
    branch: "",
    cloningStatus: {
      message: "",
      status: "UNKNOWN",
    },
    credentials: {
      id: "",
      key: "",
      name: "",
      password: "",
      token: "",
      type: "",
      user: "",
    },
    environment: "",
    environmentUrls: [],
    gitEnvironmentUrls: [],
    gitignore: [],
    healthCheckConfirm: [],
    id: "",
    includesHealthCheck: null,
    nickname: "",
    secrets: [],
    state: "ACTIVE",
    url: "",
    useVpn: false,
  },
  modalMessages,
  nicknames,
  onClose,
  onSubmitEnvs,
  onSubmitRepo,
  runTour,
  finishTour,
}: IManagementModalProps): JSX.Element => {
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateRootState: boolean = permissions.can(
    "api_mutations_update_git_root_mutate"
  );
  const { t } = useTranslation();
  const isEditing: boolean = initialValues.url !== "";

  return (
    <Modal
      onClose={onClose}
      open={true}
      title={t(`group.scope.common.${isEditing ? "edit" : "add"}`)}
    >
      <MemoryRouter
        initialEntries={[canUpdateRootState ? "/repository" : "/secrets"]}
      >
        {isEditing ? (
          <Tabs>
            <Can do={"api_mutations_update_git_root_mutate"}>
              <Tab
                id={"repoTab"}
                link={"/repository"}
                tooltip={t("group.scope.git.repo.title")}
              >
                {t("group.scope.git.repo.title")}
              </Tab>
            </Can>
            <Can do={"api_mutations_update_git_environments_mutate"}>
              <Tab
                id={"envsTab"}
                link={"/environments"}
                tooltip={t("group.scope.git.manageEnvsTooltip")}
              >
                {t("group.scope.git.envUrls")}
              </Tab>
            </Can>
            <Can do={"api_resolvers_git_root_secrets_resolve"}>
              <Tab
                id={"secretsTab"}
                link={"/secrets"}
                tooltip={t("group.scope.git.repo.title")}
              >
                {"Secrets"}
              </Tab>
            </Can>
          </Tabs>
        ) : undefined}
        <TabContent>
          <Switch>
            <Route path={"/repository"}>
              <ConfirmDialog
                message={t("group.scope.git.confirmBranch")}
                title={t("group.scope.common.confirm")}
              >
                {(confirm): React.ReactNode => {
                  async function confirmAndSubmit(
                    values: IGitRootAttr
                  ): Promise<void> {
                    if (isEditing && values.branch !== initialValues.branch) {
                      return new Promise((resolve): void => {
                        confirm(
                          (): void => {
                            resolve(onSubmitRepo(values));
                          },
                          (): void => {
                            resolve();
                          }
                        );
                      });
                    }

                    return onSubmitRepo(values);
                  }

                  return (
                    <Repository
                      finishTour={finishTour}
                      groupName={groupName}
                      initialValues={initialValues}
                      isEditing={isEditing}
                      modalMessages={modalMessages}
                      nicknames={nicknames}
                      onClose={onClose}
                      onSubmit={confirmAndSubmit}
                      runTour={runTour}
                    />
                  );
                }}
              </ConfirmDialog>
            </Route>
            <Route path={"/environments"}>
              <Environments
                modalMessages={modalMessages}
                onClose={onClose}
                onSubmit={onSubmitEnvs}
                rootInitialValues={initialValues}
              />
            </Route>
            <Route path={"/secrets"}>
              <Secrets gitRootId={initialValues.id} groupName={groupName} />
            </Route>
          </Switch>
        </TabContent>
      </MemoryRouter>
    </Modal>
  );
};

export { ManagementModal };
