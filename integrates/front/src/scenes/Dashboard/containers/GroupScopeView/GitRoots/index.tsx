import { ADD_GIT_ROOT } from "../query";
import { Button } from "components/Button";
import { ButtonToolbarRow } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { DataTableNext } from "components/DataTableNext";
import { GitRootsModal } from "./modal";
import { Glyphicon } from "react-bootstrap";
import React from "react";
import { useMutation } from "@apollo/react-hooks";
import { useTranslation } from "react-i18next";
import type { IGitFormAttr, IGitRootAttr } from "../types";

interface IGitRootsProps {
  groupName: string;
  roots: IGitRootAttr[];
}

export const GitRoots: React.FC<IGitRootsProps> = ({
  groupName,
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
  const [addGitRoot] = useMutation(ADD_GIT_ROOT);

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
