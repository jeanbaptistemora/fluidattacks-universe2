import { IVulnDataType } from "scenes/Dashboard/components/Vulnerabilities/types";
import _ from "lodash";

const sortTags: (tags: string) => string[] = (tags: string): string[] => {
  const tagSplit: string[] = tags.trim().split(",");

  return tagSplit.map((tag: string): string => tag.trim());
};

const groupExternalBts: (vulnerabilities: IVulnDataType[]) => string = (
  vulnerabilities: IVulnDataType[]
): string => {
  const bts: string = vulnerabilities.reduce(
    (acc: string, vuln: IVulnDataType): string =>
      _.isEmpty(vuln.externalBts) ? acc : vuln.externalBts,
    ""
  );

  return vulnerabilities.every((row: IVulnDataType): boolean =>
    _.isEmpty(row.externalBts) ? true : row.externalBts === bts
  )
    ? bts
    : "";
};

export { groupExternalBts, sortTags };
