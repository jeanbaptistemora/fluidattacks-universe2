/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { ITagProps } from "components/Tag";

const statusBlueColor: string[] = ["App", "Code", "Infra"];
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
  "Masked",
  "New",
  "On_hold",
  "Pending",
  "Pending verification",
  "Partially closed",
  "Permanently accepted",
  "Requested",
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
  if (statusGreenColor.includes(value)) return "green";
  if (statusOrangeColor.includes(value)) return "orange";
  if (statusRedColor.includes(value)) return "red";

  return statusBlueColor.includes(value) ? "blue" : "gray";
};

export { getBgColor };
