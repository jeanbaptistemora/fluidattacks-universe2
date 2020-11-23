import { Button } from "components/Button";
import { ButtonToolbarRow } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { DataTableNext } from "components/DataTableNext";
import { Glyphicon } from "react-bootstrap";
import type { IGitRootAttr } from "../types";
import React from "react";
import { useTranslation } from "react-i18next";

interface IGitRootsProps {
  roots: IGitRootAttr[];
}

export const GitRoots: React.FC<IGitRootsProps> = ({
  roots,
}: IGitRootsProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <React.Fragment>
      <ButtonToolbarRow>
        <Can do={"backend_api_mutations_add_git_root_mutate"}>
          <Button>
            <Glyphicon glyph={"plus"} />
            &nbsp;{t("group.scope.git.add")}
          </Button>
        </Can>
      </ButtonToolbarRow>
      <DataTableNext
        bordered={false}
        dataset={roots}
        exportCsv={false}
        headers={[
          { dataField: "url", header: t("group.scope.git.url") },
          { dataField: "branch", header: t("group.scope.git.branch") },
        ]}
        id={"tblGitRoots"}
        pageSize={15}
        search={true}
        striped={true}
      />
    </React.Fragment>
  );
};
