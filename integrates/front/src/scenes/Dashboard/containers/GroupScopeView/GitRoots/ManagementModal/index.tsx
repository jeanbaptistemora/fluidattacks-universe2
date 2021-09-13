import React from "react";
import { useTranslation } from "react-i18next";
import { MemoryRouter, Route, Switch } from "react-router-dom";

import { Environments } from "./environments";
import { Repository } from "./repository";

import type { IGitRootAttr } from "../../types";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Modal } from "components/Modal";
import { ContentTab } from "scenes/Dashboard/components/ContentTab";
import { TabsContainer } from "styles/styledComponents";
import { Can } from "utils/authz/Can";

interface IManagementModalProps {
  initialValues: IGitRootAttr | undefined;
  nicknames: string[];
  onClose: () => void;
  onSubmitEnvs: (values: IGitRootAttr) => Promise<void>;
  onSubmitRepo: (values: IGitRootAttr) => Promise<void>;
}

const ManagementModal: React.FC<IManagementModalProps> = ({
  initialValues = {
    __typename: "GitRoot",
    branch: "",
    cloningStatus: {
      message: "",
      status: "UNKNOWN",
    },
    environment: "",
    environmentUrls: [],
    gitignore: [],
    id: "",
    includesHealthCheck: false,
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
      headerTitle={t(`group.scope.common.${isEditing ? "edit" : "add"}`)}
      onEsc={onClose}
      open={true}
    >
      <MemoryRouter initialEntries={["/repository"]}>
        {isEditing ? (
          <TabsContainer>
            <ContentTab
              icon={"icon pe-7s-note2"}
              id={"repoTab"}
              link={"/repository"}
              title={t("group.scope.git.repo.title")}
              tooltip={t("group.scope.git.repo.title")}
            />
            <Can do={"api_mutations_update_git_environments_mutate"}>
              <ContentTab
                icon={"icon pe-7s-cloud"}
                id={"envsTab"}
                link={"/environments"}
                title={t("group.scope.git.envUrls")}
                tooltip={t("group.scope.git.manageEnvsTooltip")}
              />
            </Can>
          </TabsContainer>
        ) : undefined}
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
      </MemoryRouter>
    </Modal>
  );
};

export { ManagementModal };
