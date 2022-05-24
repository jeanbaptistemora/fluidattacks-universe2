import _ from "lodash";

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

export { mergeObjectArrays };
