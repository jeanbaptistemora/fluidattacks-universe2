import React from "react";
import { useRouteMatch } from "react-router-dom";

import { TableLinkButton } from "./styles";

interface ITableLinkProps {
  to: string;
  value: string;
}

const TableLink: React.FC<ITableLinkProps> = ({
  to,
  value,
}: Readonly<ITableLinkProps>): JSX.Element => {
  const { url } = useRouteMatch();

  return (
    <TableLinkButton isNone={value === "None"} to={`${url}/${to}`}>
      {value}
    </TableLinkButton>
  );
};

export type { ITableLinkProps };
export { TableLink };
