import { Label } from "react-bootstrap";
import React from "react";
import { default as style } from "../index.css";

const getBgColor: (value: string) => string = (value: string): string => {
  switch (value) {
    // Gray
    case "Requested":
      return "#707070";
    // Green
    case "Active":
    case "Closed":
    case "Enabled":
    case "Secure":
    case "Solved":
    case "Submitted":
    case "Success":
    case "Verified (closed)":
      return "#259800";
    // Orange
    case "Created":
    case "Partially closed":
      return "#FFBF00";
    // Red
    case "Disabled":
    case "Failed":
    case "Inactive":
    case "Open":
    case "Rejected":
    case "Unsolved":
    case "Verified (open)":
    case "Vulnerable":
      return "#FF2222";
    default:
      return "";
  }
};

export const statusFormatter: (value: string) => React.ReactElement<Label> = (
  value: string
): React.ReactElement<Label> => {
  const bgColor: string = getBgColor(value);

  return (
    // Need it to override default styles from react-bootstrap
    // eslint-disable-next-line react/forbid-component-props
    <Label className={style.label} style={{ backgroundColor: bgColor }}>
      {value}
    </Label>
  );
};
