import type { ITagProps } from "components/Tag";

const statusBlueColor: string[] = ["App", "Code", "Infra"];
const statusGreenColor: string[] = [
  "Active",
  "Closed",
  "Confirmed",
  "Enabled",
  "Ok",
  "Registered",
  "Safe",
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
  "Untreated",
];
const statusRedColor: string[] = [
  "Disabled",
  "Failed",
  "Inactive",
  "Open",
  "Rejected",
  "Unregistered",
  "Unsolved",
  "Verified (open)",
  "Vulnerable",
  "Vulnerable",
];

const getBgColor = (value: string): ITagProps["variant"] => {
  if (statusGreenColor.includes(value)) return "green";
  if (statusOrangeColor.includes(value)) return "orange";
  if (statusRedColor.includes(value)) return "red";

  return statusBlueColor.includes(value) ? "blue" : "gray";
};

export { getBgColor };
