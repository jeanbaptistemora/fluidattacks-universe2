import type { ApolloError } from "apollo-client";
import { Button } from "components/Button";
import { ButtonToolbarRow } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { DataTableNext } from "components/DataTableNext";
import { GitRootsModal } from "./modal";
import { Glyphicon } from "react-bootstrap";
import type { GraphQLError } from "graphql";
import { Logger } from "utils/logger";
import type { PureAbility } from "@casl/ability";
import React from "react";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError } from "utils/notifications";
import { useAbility } from "@casl/react";
import { useMutation } from "@apollo/react-hooks";
import { useTranslation } from "react-i18next";
import { ADD_GIT_ROOT, UPDATE_GIT_ROOT } from "../query";
import type { IGitFormAttr, IGitRootAttr } from "../types";

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
    setCurrentRow(undefined);
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
      <ButtonToolbarRow>
        <Can do={"backend_api_mutations_add_git_root_mutate"}>
          <div className={"mb3"}>
            <Button onClick={openModal}>
              <Glyphicon glyph={"plus"} />
              &nbsp;{t("group.scope.common.add")}
            </Button>
          </div>
        </Can>
        <Can do={"backend_api_mutations_update_git_root_mutate"}>
          <div className={"mb3"}>
            <Button disabled={currentRow === undefined} onClick={openModal}>
              <Glyphicon glyph={"plus"} />
              &nbsp;{t("group.scope.common.update")}
            </Button>
          </div>
        </Can>
      </ButtonToolbarRow>
      <DataTableNext
        bordered={true}
        dataset={roots}
        exportCsv={false}
        headers={[
          { dataField: "url", header: t("group.scope.git.repo.url") },
          { dataField: "branch", header: t("group.scope.git.repo.branch") },
          {
            dataField: "environment",
            header: t("group.scope.git.repo.environment"),
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
