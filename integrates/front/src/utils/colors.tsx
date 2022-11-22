/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { ITagProps } from "components/Tag";

const statusGrayColor: string[] = ["Requested", "Unknown", "N/a", "Queued"];
const statusGreenColor: string[] = [
  "Active",
  "Closed",
  "Confirmed",
  "Enabled",
  "Ok",
  "Registered",
  "Secure",
  "Solved",
  "Submitted",
  "Success",
  "Verified (closed)",
];
const statusOrangeColor: string[] = [
  "Accepted",
  "Cloning",
  "Created",
  "In progress",
  "New",
  "On_hold",
  "Pending",
  "Pending verification",
  "Partially closed",
  "Permanently accepted",
  "Temporarily accepted",
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

const getBgColor = (value: string): ITagProps["variant"] => {
  if (statusGrayColor.includes(value)) {
    return "gray";
  } else if (statusGreenColor.includes(value)) {
    return "green";
  } else if (statusOrangeColor.includes(value)) {
    return "orange";
  } else if (statusRedColor.includes(value)) {
    return "red";
  }

  return "gray";
};

export { getBgColor };
