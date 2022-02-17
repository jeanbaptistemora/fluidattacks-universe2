import _ from "lodash";

import type { IFilterSet, IToeLinesData } from "./types";

import {
  filterDateRange,
  filterSearchText,
  filterSelect,
} from "components/DataTableNext/utils/filters";

const getToeLinesId: (toeLinesData: IToeLinesData) => string = (
  toeLinesData: IToeLinesData
): string => toeLinesData.rootId + toeLinesData.filename;

const getToeLinesIds: (toeLines: IToeLinesData[]) => string[] = (
  toeLines: IToeLinesData[]
): string[] =>
  toeLines.map((toeLinesData: IToeLinesData): string =>
    getToeLinesId(toeLinesData)
  );

const getToeLinesIndex: (
  selectedToeLinesDatas: IToeLinesData[],
  allToeLinesDatas: IToeLinesData[]
) => number[] = (
  selectedToeLinesDatas: IToeLinesData[],
  allToeLinesDatas: IToeLinesData[]
): number[] => {
  const selectToeLinesIds: string[] = getToeLinesIds(selectedToeLinesDatas);

  return allToeLinesDatas.reduce(
    (
      selectedToeLinesIndex: number[],
      currentToeLinesData: IToeLinesData,
      currentToeLinesDataIndex: number
    ): number[] =>
      selectToeLinesIds.includes(getToeLinesId(currentToeLinesData))
        ? [...selectedToeLinesIndex, currentToeLinesDataIndex]
        : selectedToeLinesIndex,
    []
  );
};

const onSelectSeveralToeLinesHelper = (
  isSelect: boolean,
  toeLinesDatasSelected: IToeLinesData[],
  selectedToeLinesDatas: IToeLinesData[],
  setSelectedToeLines: (value: React.SetStateAction<IToeLinesData[]>) => void
): string[] => {
  if (isSelect) {
    const toeLinesToSet: IToeLinesData[] = Array.from(
      new Set([...selectedToeLinesDatas, ...toeLinesDatasSelected])
    );
    setSelectedToeLines(toeLinesToSet);

    return toeLinesToSet.map((toeLinesData: IToeLinesData): string =>
      getToeLinesId(toeLinesData)
    );
  }
  const toeLinesIds: string[] = getToeLinesIds(toeLinesDatasSelected);
  setSelectedToeLines(
    Array.from(
      new Set(
        selectedToeLinesDatas.filter(
          (selectedToeLinesData: IToeLinesData): boolean =>
            !toeLinesIds.includes(getToeLinesId(selectedToeLinesData))
        )
      )
    )
  );

  return selectedToeLinesDatas.map((toeLinesData: IToeLinesData): string =>
    getToeLinesId(toeLinesData)
  );
};

function getNonSelectable(toeLinesDatas: IToeLinesData[]): number[] {
  const nonSelectable: number[] = toeLinesDatas.reduce(
    (
      nonSelectableToeLinesDatas: number[],
      toeLinesData: IToeLinesData,
      currentToeLinesDataIndex: number
    ): number[] =>
      toeLinesData.bePresent
        ? nonSelectableToeLinesDatas
        : [...nonSelectableToeLinesDatas, currentToeLinesDataIndex],
    []
  );

  return nonSelectable;
}

const filterBooleanValue: (
  filterGroupToeLinesTable: IFilterSet,
  filterName: keyof IFilterSet,
  toeLines: IToeLinesData[],
  columnKey: keyof IToeLinesData
) => IToeLinesData[] = (
  filterGroupToeLinesTable: IFilterSet,
  filterName: keyof IFilterSet,
  toeLines: IToeLinesData[],
  columnKey: keyof IToeLinesData
): IToeLinesData[] => {
  const filterValue = _.isEmpty(filterGroupToeLinesTable[filterName])
    ? undefined
    : filterGroupToeLinesTable[filterName] === "true";

  return _.isUndefined(filterValue)
    ? toeLines
    : toeLines.filter((toeLinesData): boolean => {
        return toeLinesData[columnKey] === filterValue;
      });
};

const filterPriority: (
  filterGroupToeLinesTable: IFilterSet,
  toeLines: IToeLinesData[]
) => IToeLinesData[] = (
  filterGroupToeLinesTable: IFilterSet,
  toeLines: IToeLinesData[]
): IToeLinesData[] => {
  const priorityMax = parseFloat(filterGroupToeLinesTable.priority.max);
  const priorityMin = parseFloat(filterGroupToeLinesTable.priority.min);
  const filteredPriorityMax: IToeLinesData[] = isNaN(priorityMax)
    ? toeLines
    : toeLines.filter((toeLinesData): boolean => {
        return (
          toeLinesData.sortsRiskLevel >= 0 &&
          toeLinesData.sortsRiskLevel <= priorityMax
        );
      });

  return isNaN(priorityMin)
    ? filteredPriorityMax
    : filteredPriorityMax.filter((toeLinesData): boolean => {
        return (
          toeLinesData.sortsRiskLevel >= 0 &&
          priorityMin <= toeLinesData.sortsRiskLevel
        );
      });
};

const filterSearchtextResult: (
  searchTextFilter: string,
  toeLines: IToeLinesData[]
) => IToeLinesData[] = (
  searchTextFilter: string,
  toeLines: IToeLinesData[]
): IToeLinesData[] => filterSearchText(toeLines, searchTextFilter);

const getFilteredData: (
  filterGroupToeLinesTable: IFilterSet,
  searchTextFilter: string,
  toeLines: IToeLinesData[]
) => IToeLinesData[] = (
  filterGroupToeLinesTable: IFilterSet,
  searchTextFilter: string,
  toeLines: IToeLinesData[]
): IToeLinesData[] => {
  const filteredBePresent = filterBooleanValue(
    filterGroupToeLinesTable,
    "bePresent",
    toeLines,
    "bePresent"
  );
  const filteredFilenameExtensions: IToeLinesData[] = filterSelect(
    toeLines,
    filterGroupToeLinesTable.filenameExtension,
    "extension"
  );
  const filteredHasVulnerabilities = filterBooleanValue(
    filterGroupToeLinesTable,
    "hasVulnerabilities",
    toeLines,
    "hasVulnerabilities"
  );
  const filteredModifiedDate: IToeLinesData[] = filterDateRange(
    toeLines,
    filterGroupToeLinesTable.modifiedDate,
    "modifiedDate"
  );
  const filteredPriority = filterPriority(filterGroupToeLinesTable, toeLines);
  const filteredRoot: IToeLinesData[] = filterSelect(
    toeLines,
    filterGroupToeLinesTable.root,
    "rootNickname"
  );
  const filteredSearchtextResult = filterSearchtextResult(
    searchTextFilter,
    toeLines
  );
  const filteredData: IToeLinesData[] = _.intersection(
    filteredBePresent,
    filteredFilenameExtensions,
    filteredHasVulnerabilities,
    filteredModifiedDate,
    filteredPriority,
    filteredRoot,
    filteredSearchtextResult
  );

  return filteredData;
};

export {
  getFilteredData,
  getNonSelectable,
  getToeLinesIndex,
  onSelectSeveralToeLinesHelper,
};
