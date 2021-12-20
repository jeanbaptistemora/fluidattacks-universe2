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
    return "bg-lbl-orange";
  } else if (statusRedColor.includes(value)) {
    return "bg-lbl-red";
  }

  return "";
};

export { getBgColor };
