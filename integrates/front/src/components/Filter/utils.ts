import type { IFilter } from "./types";

function getMappedOptions(
  filter: IFilter<object>,
  dataset?: object[]
):
  | {
      header: string;
      value: string;
    }[]
  | undefined {
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
