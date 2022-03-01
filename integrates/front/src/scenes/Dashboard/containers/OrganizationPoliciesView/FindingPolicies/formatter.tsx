import _ from "lodash";
import React from "react";

import { Point } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";

const getBgColor: (value: string) => string = (value: string): string => {
  if (value === "Submitted" || value === "Inactive") {
    return "bg-lbl-gray";
  } else if (value === "Approved") {
    return "bg-lbl-green";
  } else if (value === "Rejected") {
    return "bg-lbl-red";
  }

  return "";
};

const statusFormatter: (value: string) => JSX.Element = (
  value: string
): JSX.Element => {
  const capitalizedValue: string = _.capitalize(value);
  const bgColor: string = getBgColor(capitalizedValue);

  return (
    <React.StrictMode>
      <span className={"br0 dib pa1"}>
        {/* Use className to override default styles */}
        {/* eslint-disable-next-line react/forbid-component-props */}
        <Point className={`v-mid ${bgColor}`}>
          {capitalizedValue.split(" ")[0]}
        </Point>
      </span>
    </React.StrictMode>
  );
};

export { getBgColor, statusFormatter };
