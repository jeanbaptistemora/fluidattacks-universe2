import React from "react";
import { useTranslation } from "react-i18next";

import { Container } from "./styles";

import type { IIPRootAttr } from "../types";
import { DataTableNext } from "components/DataTableNext";

interface IIPRootsProps {
  roots: IIPRootAttr[];
}

export const IPRoots: React.FC<IIPRootsProps> = ({
  roots,
}: IIPRootsProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <React.Fragment>
      <h2>{t("group.scope.ip.title")}</h2>
      <Container>
        <DataTableNext
          bordered={true}
          columnToggle={true}
          dataset={roots}
          exportCsv={true}
          headers={[
            {
              dataField: "url",
              header: t("group.scope.ip.address"),
            },
            {
              dataField: "port",
              header: t("group.scope.ip.port"),
            },
          ]}
          id={"tblIPRoots"}
          pageSize={15}
          search={true}
          striped={true}
        />
      </Container>
    </React.Fragment>
  );
};
