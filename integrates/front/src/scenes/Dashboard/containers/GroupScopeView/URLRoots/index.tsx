import React from "react";
import { useTranslation } from "react-i18next";

import { Container } from "./styles";

import type { IURLRootAttr } from "../types";
import { DataTableNext } from "components/DataTableNext";

interface IURLRootsProps {
  roots: IURLRootAttr[];
}

export const URLRoots: React.FC<IURLRootsProps> = ({
  roots,
}: IURLRootsProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <React.Fragment>
      <h2>{t("group.scope.url.title")}</h2>
      <Container>
        <DataTableNext
          bordered={true}
          columnToggle={true}
          dataset={roots}
          exportCsv={true}
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
          ]}
          id={"tblURLRoots"}
          pageSize={15}
          search={true}
          striped={true}
        />
      </Container>
    </React.Fragment>
  );
};
