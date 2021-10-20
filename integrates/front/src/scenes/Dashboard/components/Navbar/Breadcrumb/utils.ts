import _ from "lodash";

export const stylizeBreadcrumbItem: (item: string) => string = (
  item: string
): string => {
  if (/^F?\d{3}./u.exec(item)) {
    // In case of a finding title (i.e. "083. XML injection (XXE)")
    return item;
  }
  switch (item) {
    case "devsecops":
      return "DevSecOps";
    case "vulns":
      return "Vulnerabilities";
    default:
      return _.capitalize(item);
  }
};
