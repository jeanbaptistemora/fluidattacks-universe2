export const addUniqueKeys: (
  dataset: readonly Readonly<Record<string, unknown>>[]
) => Record<string, unknown>[] = (
  dataset: readonly Readonly<Record<string, unknown>>[]
): Record<string, unknown>[] => {
  return dataset.map(
    (
      data: Readonly<Record<string, unknown>>,
      index: number
    ): Record<string, unknown> => {
      return { ...data, uniqueId: index };
    }
  );
};
