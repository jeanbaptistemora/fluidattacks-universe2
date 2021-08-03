import { useMutation } from "@apollo/client";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { ManagementModal } from "./ManagementModal";
import { Container } from "./styles";

import { ADD_IP_ROOT } from "../queries";
import type { IIPRootAttr } from "../types";
import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import { Can } from "utils/authz/Can";
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

  const [isManagingRoot, setManagingRoot] =
    useState<false | { mode: "ADD" }>(false);
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
      port,
    }: {
      address: string;
      port: number;
    }): Promise<void> => {
      await addIpRoot({ variables: { address, groupName, port } });
    },
    [addIpRoot, groupName]
  );

  return (
    <React.Fragment>
      <h2>{t("group.scope.ip.title")}</h2>
      <Container>
        <DataTableNext
          bordered={true}
          columnToggle={true}
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
          ]}
          id={"tblIPRoots"}
          pageSize={10}
          search={true}
          striped={true}
        />
      </Container>
      {isManagingRoot === false ? undefined : (
        <ManagementModal onClose={closeModal} onSubmit={handleIpSubmit} />
      )}
    </React.Fragment>
  );
};
