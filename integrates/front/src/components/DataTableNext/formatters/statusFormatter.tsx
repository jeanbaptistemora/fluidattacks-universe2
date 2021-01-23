import React from "react";
import type { StyledComponent } from "styled-components";
import _ from "lodash";
import styled from "styled-components";

const StatusFormatter: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs<{
  className: string;
}>({
  className: "b br0 pa2 white",
})``;

const getBgColor: (value: string) => string = (value: string): string => {
  switch (value) {
    // Gray
    case "Requested":
    case "Unknown":
      return "bg-lbl-gray";
    // Green
    case "Active":
    case "Closed":
    case "Confirmed":
    case "Enabled":
    case "Ok":
    case "Secure":
    case "Solved":
    case "Submitted":
    case "Success":
    case "Verified (closed)":
      return "bg-lbl-green";
    // Orange
    case "Accepted":
    case "Created":
    case "Pending":
    case "Partially closed":
      return "bg-lbl-yellow";
    // Red
    case "Disabled":
    case "Failed":
    case "Inactive":
    case "Open":
    case "Rejected":
    case "Unsolved":
    case "Verified (open)":
    case "Vulnerable":
      return "bg-lbl-red";
    default:
      return "";
  }
};

const statusFormatter: (value: string) => JSX.Element = (
  value: string
): JSX.Element => {
  const capitalizedValue: string = _.capitalize(value);
  const bgColor: string = getBgColor(capitalizedValue);

  return (
    // Need it to override default background color
    // eslint-disable-next-line react/forbid-component-props
    <StatusFormatter className={bgColor}>
      {capitalizedValue.split(" ")[0]}
    </StatusFormatter>
  );
};

export { getBgColor, statusFormatter };
