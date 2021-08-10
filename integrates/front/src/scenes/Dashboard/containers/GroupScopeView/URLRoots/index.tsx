import { useMutation } from "@apollo/client";
import { useAbility } from "@casl/react";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { ManagementModal } from "./ManagementModal";
import { Container } from "./styles";

import { DeactivationModal } from "../deactivationModal";
import { ACTIVATE_ROOT, ADD_URL_ROOT, DEACTIVATE_ROOT } from "../queries";
import type { IURLRootAttr } from "../types";
import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import { DataTableNext } from "components/DataTableNext";
import { changeFormatter } from "components/DataTableNext/formatters";
import { pointStatusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
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
          case "Exception - Active root with the same Nickname already exists":
            msgError(t("group.scope.common.errors.duplicateNickname"));
            break;
          default:
            msgError(t("groupAlerts.errorTextsad"));
            Logger.error("Couldn't add url roots", error);
        }
      });
    },
  });
  const handleUrlSubmit = useCallback(
    async ({
      nickname,
      url,
    }: {
      nickname: string;
      url: string;
    }): Promise<void> => {
      await addUrlRoot({ variables: { groupName, nickname, url } });
    },
    [addUrlRoot, groupName]
  );

  const [activateRoot] = useMutation(ACTIVATE_ROOT, {
    onCompleted: (): void => {
      onUpdate();
    },
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        switch (error.message) {
          case "Exception - Active root with the same URL/branch already exists":
            msgError(t("group.scope.url.errors.invalid"));
            break;
          default:
            msgError(t("groupAlerts.errorTextsad"));
            Logger.error("Couldn't activate root", error);
        }
      });
    },
  });

  const [deactivationModal, setDeactivationModal] = useState({
    open: false,
    rootId: "",
  });
  const openDeactivationModal = useCallback((rootId: string): void => {
    setDeactivationModal({ open: true, rootId });
  }, []);
  const closeDeactivationModal = useCallback((): void => {
    setDeactivationModal({ open: false, rootId: "" });
  }, []);
  const [deactivateRoot] = useMutation(DEACTIVATE_ROOT, {
    onCompleted: (): void => {
      onUpdate();
      closeDeactivationModal();
    },
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        switch (error.message) {
          case "Exception - Active root with the same URL/branch already exists":
            msgError(t("group.scope.url.errors.invalid"));
            break;
          default:
            msgError(t("groupAlerts.errorTextsad"));
            Logger.error("Couldn't deactivate root", error);
        }
      });
    },
  });
  const handleDeactivationSubmit = useCallback(
    async (rootId: string, values: Record<string, string>): Promise<void> => {
      await deactivateRoot({
        variables: {
          groupName,
          id: rootId,
          other: values.other,
          reason: values.reason,
        },
      });
    },
    [deactivateRoot, groupName]
  );

  const permissions = useAbility(authzPermissionsContext);
  const canUpdateRootState = permissions.can(
    "api_mutations_update_root_state_mutate"
  );

  return (
    <React.Fragment>
      <h2>{t("group.scope.url.title")}</h2>
      <ConfirmDialog title={t("group.scope.common.confirm")}>
        {(confirm): JSX.Element => {
          const handleStateUpdate = (row: Record<string, string>): void => {
            if (row.state === "ACTIVE") {
              openDeactivationModal(row.id);
            } else {
              confirm((): void => {
                void activateRoot({ variables: { groupName, id: row.id } });
              });
            }
          };

          return (
            <Container>
              <DataTableNext
                bordered={true}
                columnToggle={false}
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
                  {
                    align: "center",
                    changeFunction: handleStateUpdate,
                    dataField: "state",
                    formatter: canUpdateRootState
                      ? changeFormatter
                      : pointStatusFormatter,
                    header: t("group.scope.common.state"),
                    width: canUpdateRootState ? "10%" : "100px",
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
      {deactivationModal.open ? (
        <DeactivationModal
          onClose={closeDeactivationModal}
          onSubmit={handleDeactivationSubmit}
          rootId={deactivationModal.rootId}
        />
      ) : undefined}
    </React.Fragment>
  );
};
