import type { ApolloError } from "@apollo/client";
import { useMutation } from "@apollo/client";
import { useAbility } from "@casl/react";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { Row } from "@tanstack/react-table";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { changeFormatter } from "./changeFormatter";
import { ManagementUrlModal } from "./ManagementModal/modal";
import { Container } from "./styles";

import { DeactivationModal } from "../deactivationModal";
import { InternalSurfaceButton } from "../InternalSurfaceButton";
import { ACTIVATE_ROOT, ADD_URL_ROOT, UPDATE_URL_ROOT } from "../queries";
import type { IURLRootAttr } from "../types";
import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Table } from "components/Table";
import type { ICellHelper } from "components/Table/types";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter";
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
  const permissions = useAbility(authzPermissionsContext);
  const { t } = useTranslation();

  const [isManagingRoot, setIsManagingRoot] = useState<
    false | { mode: "ADD" | "EDIT" }
  >(false);
  const [currentRow, setCurrentRow] = useState<IURLRootAttr | undefined>(
    undefined
  );

  const openAddModal = useCallback((): void => {
    setIsManagingRoot({ mode: "ADD" });
  }, []);
  const closeModal = useCallback((): void => {
    setIsManagingRoot(false);
    setCurrentRow(undefined);
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
          case "Exception - Error value is not valid":
            msgError(t("group.scope.url.errors.invalid"));
            break;
          case "Exception - Root with the same URL/branch already exists":
            msgError(t("group.scope.common.errors.duplicateUrl"));
            break;
          case "Exception - Invalid characters":
            msgError(t("group.scope.url.errors.invalidCharacters"));
            break;
          case "Exception - Active root with the same Nickname already exists":
            msgError(t("group.scope.common.errors.duplicateNickname"));
            break;
          case "Exception - The file has not been found":
            msgError(t("group.scope.common.errors.fileNotFound"));
            break;
          default:
            msgError(t("groupAlerts.errorTextsad"));
            Logger.error("Couldn't add url roots", error);
        }
      });
    },
  });

  const [updateUrlRoot] = useMutation(UPDATE_URL_ROOT, {
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

  const handleUrlSubmit = useCallback(
    async ({
      id,
      nickname,
      url,
    }: {
      id: string;
      nickname: string;
      url: string;
    }): Promise<void> => {
      if (isManagingRoot !== false) {
        if (isManagingRoot.mode === "ADD") {
          await addUrlRoot({
            variables: { groupName, nickname, url: url.trim() },
          });
        } else {
          await updateUrlRoot({
            variables: { groupName, nickname, rootId: id },
          });
        }
      }
    },
    [addUrlRoot, groupName, isManagingRoot, updateUrlRoot]
  );

  function handleRowClick(
    rowInfo: Row<IURLRootAttr>
  ): (event: React.FormEvent) => void {
    return (event: React.FormEvent): void => {
      if (rowInfo.original.state === "ACTIVE") {
        setCurrentRow(rowInfo.original);
        setIsManagingRoot({ mode: "EDIT" });
      }
      event.preventDefault();
    };
  }

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
          Logger.error("Couldn't activate url root", error);
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
              <Table
                columns={[
                  {
                    accessorKey: "host",
                    header: String(t("group.scope.url.host")),
                  },
                  {
                    accessorKey: "path",
                    header: String(t("group.scope.url.path")),
                  },
                  {
                    accessorKey: "port",
                    header: String(t("group.scope.url.port")),
                  },
                  {
                    accessorKey: "protocol",
                    header: String(t("group.scope.url.protocol")),
                  },
                  {
                    accessorKey: "query",
                    header: String(t("group.scope.url.query")),
                  },
                  {
                    accessorKey: "nickname",
                    header: String(t("group.scope.ip.nickname")),
                  },
                  {
                    accessorKey: "state",
                    cell: (cell: ICellHelper<IURLRootAttr>): JSX.Element =>
                      canUpdateRootState
                        ? changeFormatter(
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
                    <Can do={"api_mutations_add_url_root_mutate"}>
                      <Button onClick={openAddModal} variant={"secondary"}>
                        <FontAwesomeIcon icon={faPlus} />
                        &nbsp;{t("group.scope.common.add")}
                      </Button>
                    </Can>
                  </React.Fragment>
                }
                id={"tblURLRoots"}
                onRowClick={
                  permissions.can("api_resolvers_git_root_secrets_resolve")
                    ? handleRowClick
                    : undefined
                }
              />
            </Container>
          );
        }}
      </ConfirmDialog>
      {isManagingRoot === false ? undefined : (
        <ManagementUrlModal
          groupName={groupName}
          initialValues={
            isManagingRoot.mode === "EDIT" ? currentRow : undefined
          }
          onClose={closeModal}
          onSubmit={handleUrlSubmit}
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
