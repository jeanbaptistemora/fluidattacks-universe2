import React from "react";

import { SecretValue } from "./secretValue";

import type { IGitRootAttr } from "../../types";
import { Table } from "components/Table";

interface ISecret {
  id: string;
  key: string;
  value: string;
}
interface ISecretItem {
  id: string;
  key: string;
  value: JSX.Element;
}

interface ISecretsProps {
  initialValues: IGitRootAttr;
}

const Secrets: React.FC<ISecretsProps> = ({
  initialValues,
}: ISecretsProps): JSX.Element => {
  const secretsDataSet = initialValues.secrets.map(
    (item: ISecret): ISecretItem => {
      return {
        id: item.id,
        key: item.key,
        value: <SecretValue value={item.value} />,
      };
    }
  );

  return (
    <div>
      <Table
        dataset={secretsDataSet}
        exportCsv={false}
        headers={[
          {
            dataField: "key",
            header: "Key",
          },
          {
            dataField: "value",
            header: "Value",
          },
        ]}
        id={"tblGitRootSecrets"}
        pageSize={10}
        search={false}
      />
    </div>
  );
};

export { Secrets };
