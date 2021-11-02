import { useMutation } from "@apollo/client";
import { useAbility } from "@casl/react";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { ManagementModal } from "./ManagementModal";
import { Container } from "./styles";

import { DeactivationModal } from "../deactivationModal";
import { ACTIVATE_ROOT, ADD_IP_ROOT } from "../queries";
import type { IIPRootAttr } from "../types";
import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import { DataTableNext } from "components/DataTableNext";
import { changeFormatter } from "components/DataTableNext/formatters";
import { pointStatusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

interface IIPRootsProps {
  groupName: string;
  roots: IIPRootAttr[];
  onUpdate: () => void;
}

export const IPRoots: React.FC<IIPRootsProps> = ({
  groupName,
  roots,
  onUpdate,
}: IIPRootsProps): JSX.Element => {
  const { t } = useTranslation();

  const [isManagingRoot, setManagingRoot] = useState<false | { mode: "ADD" }>(
    false
  );
  const openAddModal = useCallback((): void => {
    setManagingRoot({ mode: "ADD" });
  }, []);
  const closeModal = useCallback((): void => {
    setManagingRoot(false);
  }, []);

  const [addIpRoot] = useMutation(ADD_IP_ROOT, {
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
            Logger.error("Couldn't add ip roots", error);
        }
      });
    },
  });
  const handleIpSubmit = useCallback(
    async ({
      address,
      nickname,
      port,
    }: {
      address: string;
      nickname: string;
      port: number;
    }): Promise<void> => {
      await addIpRoot({
        variables: { address: address.trim(), groupName, nickname, port },
      });
    },
    [addIpRoot, groupName]
  );

  const [activateRoot] = useMutation(ACTIVATE_ROOT, {
    onCompleted: (): void => {
      onUpdate();
    },
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        if (
          error.message ===
          "Exception - Active root with the same URL/branch already exists"
        ) {
          msgError(t("group.scope.url.errors.invalid"));
        } else {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.error("Couldn't activate ip root", error);
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

  const permissions = useAbility(authzPermissionsContext);
  const canUpdateRootState = permissions.can(
    "api_mutations_activate_root_mutate"
  );

  return (
    <React.Fragment>
      <h2>{t("group.scope.ip.title")}</h2>
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
                  <Can do={"api_mutations_add_ip_root_mutate"}>
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
                    dataField: "address",
                    header: t("group.scope.ip.address"),
                  },
                  {
                    dataField: "port",
                    header: t("group.scope.ip.port"),
                  },
                  {
                    dataField: "nickname",
                    header: t("group.scope.ip.nickname"),
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
                id={"tblIPRoots"}
                pageSize={10}
                search={true}
                striped={true}
              />
            </Container>
          );
        }}
      </ConfirmDialog>
      {isManagingRoot === false ? undefined : (
        <ManagementModal onClose={closeModal} onSubmit={handleIpSubmit} />
      )}
      {deactivationModal.open ? (
        <DeactivationModal
          groupName={groupName}
          onClose={closeDeactivationModal}
          onUpdate={onUpdate}
          rootId={deactivationModal.rootId}
        />
      ) : undefined}
    </React.Fragment>
  );
};
