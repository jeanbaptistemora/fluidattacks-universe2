import { useMutation } from "@apollo/client";
import { useAbility } from "@casl/react";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { ManagementModal } from "./ManagementModal";
import { Container } from "./styles";

import { DeactivationModal } from "../deactivationModal";
import { InternalSurfaceButton } from "../InternalSurfaceButton";
import { ACTIVATE_ROOT, ADD_URL_ROOT } from "../queries";
import { Secrets } from "../Secrets";
import type { IURLRootAttr } from "../types";
import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Modal } from "components/Modal";
import { Table } from "components/Table";
import { changeFormatter } from "components/Table/formatters";
import { filterSearchText } from "components/Table/utils";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter";
import { Row } from "styles/styledComponents";
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

  const [isManagingRoot, setIsManagingRoot] = useState<false | { mode: "ADD" }>(
    false
  );
  const [currentRow, setCurrentRow] = useState<IURLRootAttr | undefined>(
    undefined
  );
  const [isSecretsModalOpen, setIsSecretsModalOpen] = useState(false);

  const openAddModal = useCallback((): void => {
    setIsManagingRoot({ mode: "ADD" });
  }, []);
  const closeModal = useCallback((): void => {
    setIsManagingRoot(false);
  }, []);
  const closeSecretsModal = useCallback((): void => {
    setIsSecretsModalOpen(false);
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
      await addUrlRoot({ variables: { groupName, nickname, url: url.trim() } });
    },
    [addUrlRoot, groupName]
  );

  const handleRowClick = useCallback(
    (_0: React.SyntheticEvent, row: IURLRootAttr): void => {
      setCurrentRow(row);
      setIsSecretsModalOpen(true);
    },
    []
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
          Logger.error("Couldn't activate url root", error);
        }
      });
    },
  });

  const [deactivationModal, setDeactivationModal] = useState({
    open: false,
    rootId: "",
  });
  const [searchTextFilter, setSearchTextFilter] = useState("");
  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }
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

  const filterSearchtextResult: IURLRootAttr[] = filterSearchText(
    roots,
    searchTextFilter
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
              <Table
                columnToggle={false}
                customSearch={{
                  customSearchDefault: searchTextFilter,
                  isCustomSearchEnabled: true,
                  onUpdateCustomSearch: onSearchTextChange,
                  position: "right",
                }}
                dataset={filterSearchtextResult}
                exportCsv={true}
                extraButtons={
                  <Row>
                    <InternalSurfaceButton />
                    <Can do={"api_mutations_add_url_root_mutate"}>
                      <Button onClick={openAddModal} variant={"secondary"}>
                        <FontAwesomeIcon icon={faPlus} />
                        &nbsp;{t("group.scope.common.add")}
                      </Button>
                    </Can>
                  </Row>
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
                    dataField: "nickname",
                    header: t("group.scope.ip.nickname"),
                  },
                  {
                    changeFunction: handleStateUpdate,
                    dataField: "state",
                    formatter: canUpdateRootState
                      ? changeFormatter
                      : statusFormatter,
                    header: t("group.scope.common.state"),
                    width: canUpdateRootState ? "10%" : "100px",
                  },
                ]}
                id={"tblURLRoots"}
                pageSize={10}
                rowEvents={{ onClick: handleRowClick }}
                search={false}
              />
            </Container>
          );
        }}
      </ConfirmDialog>
      {_.isUndefined(currentRow) ? undefined : (
        <Modal
          open={isSecretsModalOpen}
          title={t("group.scope.git.repo.credentials.secrets.tittle")}
        >
          <Secrets
            gitRootId={currentRow.id}
            groupName={groupName}
            onCloseModal={closeSecretsModal}
          />
        </Modal>
      )}
      {isManagingRoot === false ? undefined : (
        <ManagementModal onClose={closeModal} onSubmit={handleUrlSubmit} />
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
