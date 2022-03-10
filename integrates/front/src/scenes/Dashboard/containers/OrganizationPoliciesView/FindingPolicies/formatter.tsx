import _ from "lodash";
import React from "react";

import type { IBadgeProps } from "components/Badge";
import { Badge } from "components/Badge";

const getBgColor = (value: string): IBadgeProps["variant"] => {
  if (value === "Submitted" || value === "Inactive") {
    return "gray";
  } else if (value === "Approved") {
    return "green";
  } else if (value === "Rejected") {
    return "red";
  }

  return "gray";
};

const statusFormatter: (value: string) => JSX.Element = (
  value: string
): JSX.Element => {
  const capitalizedValue: string = _.capitalize(value);
  const bgColor = getBgColor(capitalizedValue);

  return (
    <React.StrictMode>
      <Badge variant={bgColor}>{capitalizedValue.split(" ")[0]}</Badge>
    </React.StrictMode>
  );
};

export { getBgColor, statusFormatter };
