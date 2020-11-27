import { ADD_GIT_ROOT } from "../query";
import type { ApolloError } from "apollo-client";
import { Button } from "components/Button";
import { ButtonToolbarRow } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { DataTableNext } from "components/DataTableNext";
import { GitRootsModal } from "./modal";
import { Glyphicon } from "react-bootstrap";
import type { GraphQLError } from "graphql";
import { Logger } from "utils/logger";
import React from "react";
import { msgError } from "utils/notifications";
import { useMutation } from "@apollo/react-hooks";
import { useTranslation } from "react-i18next";
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
  const { t } = useTranslation();

  // State management
  const [isModalOpen, setModalOpen] = React.useState(false);

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

  // Event handlers
  const handleSubmit: (
    values: IGitFormAttr
  ) => Promise<void> = React.useCallback(
    async (values): Promise<void> => {
      await addGitRoot({
        variables: {
          ...values,
          filter: values.filter.policy === "NONE" ? undefined : values.filter,
          groupName,
        },
      });
    },
    [addGitRoot, groupName]
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
        striped={true}
      />
      {isModalOpen ? (
        <GitRootsModal onClose={closeModal} onSubmit={handleSubmit} />
      ) : undefined}
    </React.Fragment>
  );
};
