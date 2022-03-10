import type { IBadgeProps } from "components/Badge";

const statusGrayColor: string[] = ["Requested", "Unknown"];
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
  "On_hold",
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

const getBgColor = (value: string): IBadgeProps["variant"] => {
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
