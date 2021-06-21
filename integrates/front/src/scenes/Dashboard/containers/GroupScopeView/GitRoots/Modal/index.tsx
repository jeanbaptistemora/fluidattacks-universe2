import React from "react";
import { useTranslation } from "react-i18next";
import { MemoryRouter, Route, Switch } from "react-router-dom";

import { Environments } from "./environments";
import { Repository } from "./repository";

import type { IGitRootAttr } from "../../types";
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
  initialValues,
  nicknames,
  onClose,
  onSubmitEnvs,
  onSubmitRepo,
}: IManagementModalProps): JSX.Element => {
  const { t } = useTranslation();
  const isEditing: boolean = initialValues !== undefined;

  return (
    <Modal
      headerTitle={t(`group.scope.common.${isEditing ? "edit" : "add"}`)}
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
            <Repository
              initialValues={initialValues}
              isEditing={isEditing}
              nicknames={nicknames}
              onClose={onClose}
              onSubmit={onSubmitRepo}
            />
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
