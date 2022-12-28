import type { ApolloError } from "@apollo/client";
import { useMutation } from "@apollo/client";
import { useAbility } from "@casl/react";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { Row } from "@tanstack/react-table";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { changeFormatter as changeFormatterz } from "./changeFormatter";
import { ManagementModal } from "./ManagementModal";
import { Container } from "./styles";

import { DeactivationModal } from "../deactivationModal";
import { InternalSurfaceButton } from "../InternalSurfaceButton";
import type { IIPRootAttr } from "../types";
import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Table as Tablez } from "components/Table";
import type { ICellHelper } from "components/Table/types";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter";
import {
  ACTIVATE_ROOT,
  ADD_IP_ROOT,
  UPDATE_IP_ROOT,
} from "scenes/Dashboard/containers/Group-Content/GroupScopeView/queries";
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

  const [currentRow, setCurrentRow] = useState<IIPRootAttr | undefined>(
    undefined
  );
  const [isManagingRoot, setIsManagingRoot] = useState<
    false | { mode: "ADD" | "EDIT" }
  >(false);

  const openAddModal = useCallback((): void => {
    setIsManagingRoot({ mode: "ADD" });
  }, []);
  const closeModal = useCallback((): void => {
    setIsManagingRoot(false);
    setCurrentRow(undefined);
  }, []);

  function handleRowClick(
    rowInfo: Row<IIPRootAttr>
  ): (event: React.FormEvent) => void {
    return (event: React.FormEvent): void => {
      if (rowInfo.original.state === "ACTIVE") {
        setCurrentRow(rowInfo.original);
        setIsManagingRoot({ mode: "EDIT" });
      }
      event.preventDefault();
    };
  }

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
          case "Exception - Root with the same URL/branch already exists":
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
  const [updateIpRoot] = useMutation(UPDATE_IP_ROOT, {
    onCompleted: (): void => {
      onUpdate();
      closeModal();
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error): void => {
        switch (error.message) {
          case "Exception - Error empty value is not valid":
            msgError(t("group.scope.url.errors.invalid"));
            break;
          case "Exception - Active root with the same Nickname already exists":
            msgError(t("group.scope.common.errors.duplicateNickname"));
            break;
          default:
            msgError(t("groupAlerts.errorTextsad"));
            Logger.error("Couldn't update ip roots", error);
        }
      });
    },
  });

  const handleIpSubmit = useCallback(
    async ({
      address,
      id,
      nickname,
    }: {
      address: string;
      id: string;
      nickname: string;
    }): Promise<void> => {
      if (isManagingRoot !== false) {
        if (isManagingRoot.mode === "ADD") {
          await addIpRoot({
            variables: {
              address: address.trim(),
              groupName,
              nickname,
            },
          });
        } else {
          await updateIpRoot({
            variables: { groupName, nickname, rootId: id },
          });
        }
      }
    },
    [addIpRoot, groupName, isManagingRoot, updateIpRoot]
  );

  const [activateRoot] = useMutation(ACTIVATE_ROOT, {
    onCompleted: (): void => {
      onUpdate();
    },
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        if (
          error.message ===
          "Exception - Root with the same URL/branch already exists"
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
              <Tablez
                columns={[
                  {
                    accessorKey: "address",
                    header: String(t("group.scope.ip.address")),
                  },
                  {
                    accessorKey: "nickname",
                    header: String(t("group.scope.ip.nickname")),
                  },
                  {
                    accessorKey: "state",
                    cell: (cell: ICellHelper<IIPRootAttr>): JSX.Element =>
                      canUpdateRootState
                        ? changeFormatterz(
                            cell.row.original as unknown as Record<
                              string,
                              string
                            >,
                            handleStateUpdate
                          )
                        : statusFormatter(cell.getValue()),
                    header: String(t("group.scope.common.state")),
                  },
                ]}
                data={roots}
                extraButtons={
                  <React.Fragment>
                    <InternalSurfaceButton />
                    <Can do={"api_mutations_add_ip_root_mutate"}>
                      <Button onClick={openAddModal} variant={"secondary"}>
                        <FontAwesomeIcon icon={faPlus} />
                        &nbsp;{t("group.scope.common.add")}
                      </Button>
                    </Can>
                  </React.Fragment>
                }
                id={"tblIPRoots"}
                onRowClick={
                  permissions.can("api_mutations_update_ip_root_mutate")
                    ? handleRowClick
                    : undefined
                }
              />
            </Container>
          );
        }}
      </ConfirmDialog>
      {isManagingRoot === false ? undefined : (
        <ManagementModal
          initialValues={
            isManagingRoot.mode === "EDIT" ? currentRow : undefined
          }
          onClose={closeModal}
          onSubmit={handleIpSubmit}
        />
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
