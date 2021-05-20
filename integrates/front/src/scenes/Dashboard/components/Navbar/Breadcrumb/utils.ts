import _ from "lodash";

export const stylizeBreadcrumbItem: (item: string) => string = (
  item: string
): string => {
  switch (item) {
    case "devsecops":
      return "DevSecOps";
    case "vulns":
      return "Vulnerabilities";
    default:
      return _.capitalize(item);
  }
};
