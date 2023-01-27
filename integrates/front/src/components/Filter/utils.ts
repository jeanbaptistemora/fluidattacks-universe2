import type { IFilter, ISelectedOptions } from "./types";

function getMappedOptions(
  filter: IFilter<object>,
  dataset?: object[]
): ISelectedOptions[] | undefined {
  const options =
    typeof filter.selectOptions === "function"
      ? filter.selectOptions(dataset ?? [])
      : filter.selectOptions;

  const mappedOptions = options?.map(
    (option): { header: string; value: string } =>
      typeof option === "string" ? { header: option, value: option } : option
  );

  return mappedOptions;
}

export { getMappedOptions };
