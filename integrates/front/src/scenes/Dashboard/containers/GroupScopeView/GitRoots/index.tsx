import type { ApolloError } from "apollo-client";
import { Button } from "components/Button";
import { ButtonToolbarRow } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { ConfirmDialog } from "components/ConfirmDialog";
import { DataTableNext } from "components/DataTableNext";
import { FluidIcon } from "components/FluidIcon";
import { GitModal } from "./gitModal";
import { Glyphicon } from "react-bootstrap";
import type { GraphQLError } from "graphql";
import type { IConfirmFn } from "components/ConfirmDialog";
import type { IGitRootAttr } from "../types";
import { Logger } from "utils/logger";
import type { PureAbility } from "@casl/ability";
import React from "react";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError } from "utils/notifications";
import { useAbility } from "@casl/react";
import { useMutation } from "@apollo/react-hooks";
import { useTranslation } from "react-i18next";
import { ADD_GIT_ROOT, UPDATE_GIT_ROOT, UPDATE_ROOT_STATE } from "../query";
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
  const [isManagingRoot, setManagingRoot] = React.useState(false);
  const openModal: () => void = React.useCallback((): void => {
    setManagingRoot(true);
  }, []);

  const closeModal: () => void = React.useCallback((): void => {
    setManagingRoot(false);
  }, []);

  const [currentRow, setCurrentRow] = React.useState<IGitRootAttr | undefined>(
    undefined
  );

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
  const handleRowSelect: (
    row: IGitRootAttr
  ) => void = React.useCallback(setCurrentRow, [setCurrentRow]);

  const handleEditSubmit: (
    values: IGitRootAttr
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
            filter,
            groupName,
            includesHealthCheck,
            url,
          },
        });
      } else {
        const { environment, filter, id, includesHealthCheck } = values;
        await updateGitRoot({
          variables: {
            environment,
            filter,
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
      {isManagingRoot ? (
        <GitModal
          initialValues={currentRow}
          onClose={closeModal}
          onSubmit={handleEditSubmit}
        />
      ) : undefined}
    </React.Fragment>
  );
};
