import _ from "lodash";

import type { IFinding, IVulnerability } from "./types";

const formatLocation = (
  _cell: string,
  row: IVulnerability
): React.ReactNode => {
  return `${row.where}:${row.specific}`;
};

const formatType = (cell: IFinding[]): React.ReactNode => {
  return cell.map((finding): string => `- ${finding.title}`).join(", ");
};

const mergeObjectArrays = <T>(currentValues: T[], incomingValues: T[]): T[] => {
  return Object.values(
    _.mergeWith(
      _.keyBy(currentValues, "id"),
      _.keyBy(incomingValues, "id"),
      (value: unknown, srcValue: unknown): unknown => {
        if (_.isArray(value)) {
          return (value as unknown[]).concat(srcValue);
        }

        return undefined;
      }
    )
  );
};

export { formatLocation, formatType, mergeObjectArrays };
