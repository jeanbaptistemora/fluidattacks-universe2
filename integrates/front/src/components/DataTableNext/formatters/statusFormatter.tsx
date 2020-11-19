import type { Label } from "react-bootstrap";
import React from "react";
import type { StyledComponent } from "styled-components";
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
      return "bg-lbl-gray";
    // Green
    case "Active":
    case "Closed":
    case "Confirmed":
    case "Enabled":
    case "Secure":
    case "Solved":
    case "Submitted":
    case "Success":
    case "Verified (closed)":
      return "bg-lbl-green";
    // Orange
    case "Accepted":
    case "Created":
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

export const statusFormatter: (value: string) => React.ReactElement<Label> = (
  value: string
): React.ReactElement<Label> => {
  const bgColor: string = getBgColor(value);

  return (
    // Need it to override default background color
    // eslint-disable-next-line react/forbid-component-props
    <StatusFormatter className={bgColor}>{value}</StatusFormatter>
  );
};
