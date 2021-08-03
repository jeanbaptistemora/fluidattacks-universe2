import { useMutation } from "@apollo/client";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { ManagementModal } from "./ManagementModal";
import { Container } from "./styles";

import { ADD_URL_ROOT } from "../queries";
import type { IURLRootAttr } from "../types";
import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import { DataTableNext } from "components/DataTableNext";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

interface IURLRootsProps {
  groupName: string;
  roots: IURLRootAttr[];
  onUpdate: () => void;
}

export const URLRoots: React.FC<IURLRootsProps> = ({
  groupName,
  roots,
  onUpdate,
}: IURLRootsProps): JSX.Element => {
  const { t } = useTranslation();

  const [isManagingRoot, setManagingRoot] =
    useState<false | { mode: "ADD" }>(false);
  const openAddModal = useCallback((): void => {
    setManagingRoot({ mode: "ADD" });
  }, []);
  const closeModal = useCallback((): void => {
    setManagingRoot(false);
  }, []);

  const [addUrlRoot] = useMutation(ADD_URL_ROOT, {
    onCompleted: (): void => {
      onUpdate();
      closeModal();
    },
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        switch (error.message) {
          case "Exception - Error empty value is not valid":
            msgError(t("group.scope.url.errors.invalid"));
            break;
          case "Exception - Active root with the same URL/branch already exists":
            msgError(t("group.scope.common.errors.duplicateUrl"));
            break;
          default:
            msgError(t("groupAlerts.errorTextsad"));
            Logger.error("Couldn't add url roots", error);
        }
      });
    },
  });
  const handleUrlSubmit = useCallback(
    async ({ url }: { url: string }): Promise<void> => {
      await addUrlRoot({ variables: { groupName, url } });
    },
    [addUrlRoot, groupName]
  );

  return (
    <React.Fragment>
      <h2>{t("group.scope.url.title")}</h2>
      <ConfirmDialog title={t("group.scope.common.confirm")}>
        {(): JSX.Element => {
          return (
            <Container>
              <DataTableNext
                bordered={true}
                columnToggle={true}
                dataset={roots}
                exportCsv={true}
                extraButtons={
                  <Can do={"api_mutations_add_url_root_mutate"}>
                    <div className={"mb3"}>
                      <Button onClick={openAddModal}>
                        <FontAwesomeIcon icon={faPlus} />
                        &nbsp;{t("group.scope.common.add")}
                      </Button>
                    </div>
                  </Can>
                }
                headers={[
                  {
                    dataField: "host",
                    header: t("group.scope.url.host"),
                  },
                  {
                    dataField: "path",
                    header: t("group.scope.url.path"),
                  },
                  {
                    dataField: "port",
                    header: t("group.scope.url.port"),
                  },
                  {
                    dataField: "protocol",
                    header: t("group.scope.url.protocol"),
                  },
                ]}
                id={"tblURLRoots"}
                pageSize={10}
                search={true}
                striped={true}
              />
            </Container>
          );
        }}
      </ConfirmDialog>
      {isManagingRoot === false ? undefined : (
        <ManagementModal onClose={closeModal} onSubmit={handleUrlSubmit} />
      )}
    </React.Fragment>
  );
};
