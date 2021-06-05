import _ from "lodash";
import React from "react";

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
    <span className={`b br0 dib pa1 white ${bgColor}`}>
      {capitalizedValue.split(" ")[0]}
    </span>
  );
};

export { getBgColor, statusFormatter };
