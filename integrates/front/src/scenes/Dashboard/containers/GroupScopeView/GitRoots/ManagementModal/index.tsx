import React from "react";
import { useTranslation } from "react-i18next";
import { MemoryRouter, Route, Switch } from "react-router-dom";

import { Environments } from "./environments";
import { Repository } from "./repository";

import type { IGitRootAttr } from "../../types";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Modal } from "components/Modal";
import { ContentTab } from "scenes/Dashboard/components/ContentTab";
import { TabContent, TabsContainer } from "styles/styledComponents";
import { Can } from "utils/authz/Can";

interface IManagementModalProps {
  groupName: string;
  initialValues: IGitRootAttr | undefined;
  nicknames: string[];
  onClose: () => void;
  onSubmitEnvs: (values: IGitRootAttr) => Promise<void>;
  onSubmitRepo: (values: IGitRootAttr) => Promise<void>;
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
    gitignore: [],
    id: "",
    includesHealthCheck: null,
    nickname: "",
    state: "ACTIVE",
    url: "",
  },
  nicknames,
  onClose,
  onSubmitEnvs,
  onSubmitRepo,
}: IManagementModalProps): JSX.Element => {
  const { t } = useTranslation();
  const isEditing: boolean = initialValues.url !== "";

  return (
    <Modal
      onClose={onClose}
      open={true}
      title={t(`group.scope.common.${isEditing ? "edit" : "add"}`)}
    >
      <MemoryRouter initialEntries={["/repository"]}>
        {isEditing ? (
          <TabsContainer>
            <ContentTab
              id={"repoTab"}
              link={"/repository"}
              title={t("group.scope.git.repo.title")}
              tooltip={t("group.scope.git.repo.title")}
            />
            <Can do={"api_mutations_update_git_environments_mutate"}>
              <ContentTab
                id={"envsTab"}
                link={"/environments"}
                title={t("group.scope.git.envUrls")}
                tooltip={t("group.scope.git.manageEnvsTooltip")}
              />
            </Can>
          </TabsContainer>
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
                      groupName={groupName}
                      initialValues={initialValues}
                      isEditing={isEditing}
                      nicknames={nicknames}
                      onClose={onClose}
                      onSubmit={confirmAndSubmit}
                    />
                  );
                }}
              </ConfirmDialog>
            </Route>
            <Route path={"/environments"}>
              <Environments
                initialValues={initialValues}
                onClose={onClose}
                onSubmit={onSubmitEnvs}
              />
            </Route>
          </Switch>
        </TabContent>
      </MemoryRouter>
    </Modal>
  );
};

export { ManagementModal };
