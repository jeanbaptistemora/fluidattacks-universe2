import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import React from "react";
import { useTranslation } from "react-i18next";
import { MemoryRouter, Route, Switch } from "react-router-dom";

import { ManagementModal } from ".";
import { Secrets } from "../../Secrets";
import type { IURLRootAttr } from "../../types";
import { Modal } from "components/Modal";
import { Tab, Tabs } from "components/Tabs";
import { TabContent } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";

interface IManagementModalProps {
  groupName: string;
  initialValues: IURLRootAttr | undefined;
  onClose: () => void;
  onSubmit: (values: {
    id: string;
    nickname: string;
    url: string;
  }) => Promise<void>;
}

const ManagementUrlModal: React.FC<IManagementModalProps> = ({
  groupName,
  initialValues = {
    __typename: "URLRoot",
    host: "",
    id: "",
    nickname: "",
    path: "",
    port: 0,
    protocol: "HTTPS",
    query: "",
    state: "ACTIVE",
  },
  onClose,
  onSubmit,
}: IManagementModalProps): JSX.Element => {
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateRootState: boolean = permissions.can(
    "api_mutations_update_url_root_mutate"
  );
  const { t } = useTranslation();
  const isEditing: boolean = initialValues.host !== "";

  return (
    <Modal
      onClose={onClose}
      open={true}
      title={t(`group.scope.common.${isEditing ? "edit" : "add"}`)}
    >
      <MemoryRouter initialEntries={[canUpdateRootState ? "/url" : "/secrets"]}>
        {isEditing ? (
          <Tabs>
            <Can do={"api_mutations_update_url_root_mutate"}>
              <Tab
                id={"urlTab"}
                link={"/url"}
                tooltip={t("group.scope.url.modal.title")}
              >
                {t("group.scope.url.modal.title")}
              </Tab>
            </Can>
            <Can do={"api_resolvers_git_root_secrets_resolve"}>
              <Tab id={"secretsTab"} link={"/secrets"} tooltip={""}>
                {"Secrets"}
              </Tab>
            </Can>
          </Tabs>
        ) : undefined}
        <TabContent>
          <Switch>
            <Route path={"/url"}>
              <ManagementModal
                initialValues={initialValues}
                isEditing={isEditing}
                onClose={onClose}
                onSubmit={onSubmit}
              />
            </Route>
            <Route path={"/secrets"}>
              <Secrets
                gitRootId={initialValues.id}
                groupName={groupName}
                onCloseModal={onClose}
              />
            </Route>
          </Switch>
        </TabContent>
      </MemoryRouter>
    </Modal>
  );
};

export { ManagementUrlModal };
