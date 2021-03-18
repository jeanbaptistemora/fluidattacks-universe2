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
  className: "b br0 dib pa2 white",
})``;

const statusGrayColor: string[] = ["Requested", "Unknown"];
const statusGreenColor: string[] = [
  "Active",
  "Closed",
  "Confirmed",
  "Enabled",
  "Ok",
  "Secure",
  "Solved",
  "Submitted",
  "Success",
  "Verified (closed)",
];
const statusOrangeColor: string[] = [
  "Accepted",
  "Created",
  "Pending",
  "Partially closed",
];
const statusRedColor: string[] = [
  "Disabled",
  "Failed",
  "Inactive",
  "Open",
  "Rejected",
  "Unsolved",
  "Unregistered",
  "Verified (open)",
  "Vulnerable",
];

const getBgColor: (value: string) => string = (value: string): string => {
  if (statusGrayColor.includes(value)) {
    return "bg-lbl-gray";
  } else if (statusGreenColor.includes(value)) {
    return "bg-lbl-green";
  } else if (statusOrangeColor.includes(value)) {
    return "bg-lbl-yellow";
  } else if (statusRedColor.includes(value)) {
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
    // Need it to override default background color
    // eslint-disable-next-line react/forbid-component-props
    <StatusFormatter className={bgColor}>
      {capitalizedValue.split(" ")[0]}
    </StatusFormatter>
  );
};

export { getBgColor, statusFormatter };
