import _ from "lodash";
import React from "react";

import { TableLink } from "components/TableNew/styles";

export function formatLinkHandler(link: string, text: string): JSX.Element {
  return (
    <TableLink to={`groups/${link.toLowerCase()}`}>
      {_.capitalize(text)}
    </TableLink>
  );
}
