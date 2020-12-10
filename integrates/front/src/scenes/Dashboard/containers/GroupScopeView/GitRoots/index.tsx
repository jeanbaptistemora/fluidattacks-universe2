import type { ApolloError } from "apollo-client";
import { Button } from "components/Button";
import { ButtonToolbarRow } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { ConfirmDialog } from "components/ConfirmDialog";
import { DataTableNext } from "components/DataTableNext";
import { FluidIcon } from "components/FluidIcon";
import { GitRootsModal } from "./modal";
import { Glyphicon } from "react-bootstrap";
import type { GraphQLError } from "graphql";
import type { IConfirmFn } from "components/ConfirmDialog";
import { Logger } from "utils/logger";
import type { PureAbility } from "@casl/ability";
import React from "react";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError } from "utils/notifications";
import { useAbility } from "@casl/react";
import { useMutation } from "@apollo/react-hooks";
import { useTranslation } from "react-i18next";
import { ADD_GIT_ROOT, UPDATE_GIT_ROOT, UPDATE_ROOT_STATE } from "../query";
import type { IGitFormAttr, IGitRootAttr } from "../types";
import {
  changeFormatter,
  statusFormatter,
} from "components/DataTableNext/formatters";

interface IGitRootsProps {
  groupName: string;
  onUpdate: () => void;
  roots: IGitRootAttr[];
}

export const GitRoots: React.FC<IGitRootsProps> = ({
  groupName,
  onUpdate,
  roots,
}: IGitRootsProps): JSX.Element => {
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const { t } = useTranslation();

  // State management
  const [isModalOpen, setModalOpen] = React.useState(false);
  const [currentRow, setCurrentRow] = React.useState<IGitFormAttr | undefined>(
    undefined
  );

  const openModal: () => void = React.useCallback((): void => {
    setModalOpen(true);
  }, []);

  const closeModal: () => void = React.useCallback((): void => {
    setModalOpen(false);
  }, []);

  // GraphQL operations
  const [addGitRoot] = useMutation(ADD_GIT_ROOT, {
    onCompleted: (): void => {
      onUpdate();
      closeModal();
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        switch (error.message) {
          case "Exception - Error empty value is not valid":
            msgError(t("group.scope.git.errors.invalid"));
            break;
          case "Exception - One or more values already exist":
            msgError(t("group.scope.common.errors.duplicate"));
            break;
          default:
            msgError(t("group_alerts.error_textsad"));
            Logger.error("Couldn't add git roots", error);
        }
      });
    },
  });

  const [updateGitRoot] = useMutation(UPDATE_GIT_ROOT, {
    onCompleted: (): void => {
      onUpdate();
      closeModal();
      setCurrentRow(undefined);
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        switch (error.message) {
          case "Exception - Error empty value is not valid":
            msgError(t("group.scope.git.errors.invalid"));
            break;
          default:
            msgError(t("group_alerts.error_textsad"));
            Logger.error("Couldn't update git root", error);
        }
      });
    },
  });

  const [updateRootState] = useMutation(UPDATE_ROOT_STATE, {
    onCompleted: (): void => {
      onUpdate();
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      msgError(t("group_alerts.error_textsad"));
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't update root state", error);
      });
    },
  });

  // Event handlers
  const handleRowSelect: (row: IGitRootAttr) => void = React.useCallback(
    (row): void => {
      setCurrentRow({
        ...row,
        filter:
          row.filter === null ? { paths: [""], policy: "NONE" } : row.filter,
      });
    },
    []
  );

  const handleSubmit: (
    values: IGitFormAttr
  ) => Promise<void> = React.useCallback(
    async (values): Promise<void> => {
      if (currentRow === undefined) {
        const {
          branch,
          environment,
          filter,
          includesHealthCheck,
          url,
        } = values;
        await addGitRoot({
          variables: {
            branch,
            environment,
            filter: filter.policy === "NONE" ? undefined : values.filter,
            groupName,
            includesHealthCheck,
            url,
          },
        });
      } else {
        const {
          environment,
          filter: { paths, policy },
          id,
          includesHealthCheck,
        } = values;
        await updateGitRoot({
          variables: {
            environment,
            filter: policy === "NONE" ? undefined : { paths, policy },
            id,
            includesHealthCheck,
          },
        });
      }
    },
    [addGitRoot, currentRow, groupName, updateGitRoot]
  );

  return (
    <React.Fragment>
      <h3>{t("group.scope.git.title")}</h3>
      <ButtonToolbarRow>
        <Can do={"backend_api_mutations_add_git_root_mutate"}>
          <div className={"mb3"}>
            <Button id={"git-root-add"} onClick={openModal}>
              <Glyphicon glyph={"plus"} />
              &nbsp;{t("group.scope.common.add")}
            </Button>
          </div>
        </Can>
        <Can do={"backend_api_mutations_update_git_root_mutate"}>
          <div className={"mb3"}>
            <Button disabled={currentRow === undefined} onClick={openModal}>
              <FluidIcon icon={"edit"} />
              &nbsp;{t("group.scope.common.edit")}
            </Button>
          </div>
        </Can>
      </ButtonToolbarRow>
      <ConfirmDialog title={t("group.scope.common.confirm")}>
        {(confirm: IConfirmFn): React.ReactNode => {
          const handleStateUpdate: (row: Record<string, string>) => void = (
            row
          ): void => {
            confirm((): void => {
              void updateRootState({
                variables: {
                  id: row.id,
                  state: row.state === "ACTIVE" ? "INACTIVE" : "ACTIVE",
                },
              });
            });
          };

          return (
            <DataTableNext
              bordered={true}
              dataset={roots}
              exportCsv={false}
              headers={[
                { dataField: "url", header: t("group.scope.git.repo.url") },
                {
                  dataField: "branch",
                  header: t("group.scope.git.repo.branch"),
                },
                {
                  dataField: "environment",
                  header: t("group.scope.git.repo.environment"),
                },
                {
                  align: "center",
                  changeFunction: handleStateUpdate,
                  dataField: "state",
                  formatter: permissions.can(
                    "backend_api_mutations_update_root_state_mutate"
                  )
                    ? changeFormatter
                    : statusFormatter,
                  header: t("group.scope.common.state"),
                },
              ]}
              id={"tblGitRoots"}
              pageSize={15}
              search={true}
              selectionMode={{
                clickToSelect: false,
                hideSelectColumn: permissions.cannot(
                  "backend_api_mutations_update_git_root_mutate"
                ),
                mode: "radio",
                onSelect: handleRowSelect,
              }}
              striped={true}
            />
          );
        }}
      </ConfirmDialog>
      {isModalOpen ? (
        <GitRootsModal
          initialValues={currentRow}
          onClose={closeModal}
          onSubmit={handleSubmit}
        />
      ) : undefined}
    </React.Fragment>
  );
};
