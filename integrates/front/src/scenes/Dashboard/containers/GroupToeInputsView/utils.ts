import _ from "lodash";

import type { IFilterSet, IToeInputData } from "./types";

import {
  filterSearchText,
  filterSelect,
} from "components/DataTableNext/utils/filters";

const getToeInputId: (toeInputData: IToeInputData) => string = (
  toeInputData: IToeInputData
): string =>
  toeInputData.unreliableRootNickname +
  toeInputData.component +
  toeInputData.entryPoint;

const getToeInputIds: (toeInputs: IToeInputData[]) => string[] = (
  toeInputs: IToeInputData[]
): string[] =>
  toeInputs.map((toeInputData: IToeInputData): string =>
    getToeInputId(toeInputData)
  );

const getToeInputIndex: (
  selectedToeInputDatas: IToeInputData[],
  allToeInputDatas: IToeInputData[]
) => number[] = (
  selectedToeInputDatas: IToeInputData[],
  allToeInputDatas: IToeInputData[]
): number[] => {
  const selectToeInputIds: string[] = getToeInputIds(selectedToeInputDatas);

  return allToeInputDatas.reduce(
    (
      selectedToeInputIndex: number[],
      currentToeInputData: IToeInputData,
      currentToeInputDataIndex: number
    ): number[] =>
      selectToeInputIds.includes(getToeInputId(currentToeInputData))
        ? [...selectedToeInputIndex, currentToeInputDataIndex]
        : selectedToeInputIndex,
    []
  );
};

const onSelectSeveralToeInputHelper = (
  isSelect: boolean,
  toeInputDatasSelected: IToeInputData[],
  selectedToeInputDatas: IToeInputData[],
  setSelectedToeInput: (value: React.SetStateAction<IToeInputData[]>) => void
): string[] => {
  if (isSelect) {
    const toeInputsToSet: IToeInputData[] = Array.from(
      new Set([...selectedToeInputDatas, ...toeInputDatasSelected])
    );
    setSelectedToeInput(toeInputsToSet);

    return toeInputsToSet.map((toeInputData: IToeInputData): string =>
      getToeInputId(toeInputData)
    );
  }
  const toeInputIds: string[] = getToeInputIds(toeInputDatasSelected);
  setSelectedToeInput(
    Array.from(
      new Set(
        selectedToeInputDatas.filter(
          (selectedToeInputData: IToeInputData): boolean =>
            !toeInputIds.includes(getToeInputId(selectedToeInputData))
        )
      )
    )
  );

  return selectedToeInputDatas.map((toeInputData: IToeInputData): string =>
    getToeInputId(toeInputData)
  );
};

const filterBePresent: (
  filterGroupToeInputTable: IFilterSet,
  toeInputs: IToeInputData[]
) => IToeInputData[] = (
  filterGroupToeInputTable: IFilterSet,
  toeInputs: IToeInputData[]
): IToeInputData[] => {
  const bePresent = filterGroupToeInputTable.bePresent === "true";

  return _.isEmpty(filterGroupToeInputTable.bePresent)
    ? toeInputs
    : toeInputs.filter((toeInputData): boolean => {
        return toeInputData.bePresent === bePresent;
      });
};
const filterHasVulnerabilities: (
  filterGroupToeInputTable: IFilterSet,
  toeInputs: IToeInputData[]
) => IToeInputData[] = (
  filterGroupToeInputTable: IFilterSet,
  toeInputs: IToeInputData[]
): IToeInputData[] => {
  const hasVulnerabilities =
    filterGroupToeInputTable.hasVulnerabilities === "true";

  return _.isEmpty(filterGroupToeInputTable.hasVulnerabilities)
    ? toeInputs
    : toeInputs.filter((toeInputData): boolean => {
        return toeInputData.hasVulnerabilities === hasVulnerabilities;
      });
};
const filterRoot: (
  filterGroupToeInputTable: IFilterSet,
  toeInput: IToeInputData[]
) => IToeInputData[] = (
  filterGroupToeInputTable: IFilterSet,
  toeInput: IToeInputData[]
): IToeInputData[] =>
  _.isEmpty(filterGroupToeInputTable.root)
    ? toeInput
    : toeInput.filter((toeInputData): boolean => {
        return (
          toeInputData.markedRootNickname === filterGroupToeInputTable.root
        );
      });

const filterSearchtextResult: (
  searchTextFilter: string,
  toeInputs: IToeInputData[]
) => IToeInputData[] = (
  searchTextFilter: string,
  toeInputs: IToeInputData[]
): IToeInputData[] => filterSearchText(toeInputs, searchTextFilter);

const getFilteredData: (
  filterGroupToeInputTable: IFilterSet,
  searchTextFilter: string,
  toeInput: IToeInputData[]
) => IToeInputData[] = (
  filterGroupToeInputTable: IFilterSet,
  searchTextFilter: string,
  toeInput: IToeInputData[]
): IToeInputData[] => {
  const filteredBePresent = filterBePresent(filterGroupToeInputTable, toeInput);
  const filteredComponent: IToeInputData[] = filterSelect(
    toeInput,
    filterGroupToeInputTable.component,
    "component"
  );
  const filteredHasVulnerabilities = filterHasVulnerabilities(
    filterGroupToeInputTable,
    toeInput
  );
  const filteredRoot = filterRoot(filterGroupToeInputTable, toeInput);
  const filteredSearchtextResult = filterSearchtextResult(
    searchTextFilter,
    toeInput
  );
  const filteredData: IToeInputData[] = _.intersection(
    filteredBePresent,
    filteredComponent,
    filteredHasVulnerabilities,
    filteredRoot,
    filteredSearchtextResult
  );

  return filteredData;
};

export { getFilteredData, getToeInputIndex, onSelectSeveralToeInputHelper };
