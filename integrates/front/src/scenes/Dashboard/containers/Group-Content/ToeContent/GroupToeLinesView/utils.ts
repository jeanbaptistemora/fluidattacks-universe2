import _ from "lodash";

import { filterDateRange, filterSearchText, filterSelect } from "./filters";
import type {
  IFilterSet,
  IToeLinesAttr,
  IToeLinesData,
  IToeLinesEdge,
} from "./types";

import type { IFilter } from "components/Filter";

const NOEXTENSION = ".no.extension.";
const PERCENTBASE = 100;
const COMMIT_LENGTH = 7;

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

const filterCoverage: (
  filterGroupToeLinesTable: IFilterSet,
  toeLines: IToeLinesData[]
) => IToeLinesData[] = (
  filterGroupToeLinesTable: IFilterSet,
  toeLines: IToeLinesData[]
): IToeLinesData[] => {
  const coverageMax =
    parseFloat(filterGroupToeLinesTable.coverage.max) / PERCENTBASE;
  const coverageMin =
    parseFloat(filterGroupToeLinesTable.coverage.min) / PERCENTBASE;
  const filteredcoverageMax: IToeLinesData[] = isNaN(coverageMax)
    ? toeLines
    : toeLines.filter((toeLinesData): boolean => {
        return toeLinesData.coverage <= coverageMax;
      });

  return isNaN(coverageMin)
    ? filteredcoverageMax
    : filteredcoverageMax.filter((toeLinesData): boolean => {
        return coverageMin <= toeLinesData.coverage;
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
  const filteredCoverage: IToeLinesData[] = filterCoverage(
    filterGroupToeLinesTable,
    toeLines
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
  const filteredSearchtextResult = filterSearchtextResult(
    searchTextFilter,
    toeLines
  );
  const filteredSeenAt: IToeLinesData[] = filterDateRange(
    toeLines,
    filterGroupToeLinesTable.seenAt,
    "seenAt"
  );
  const filteredData: IToeLinesData[] = _.intersection(
    filteredCoverage,
    filteredFilenameExtensions,
    filteredHasVulnerabilities,
    filteredModifiedDate,
    filteredPriority,
    filteredSearchtextResult,
    filteredSeenAt
  );

  return filteredData;
};

const formatBePresent = (bePresent: string): boolean | undefined =>
  bePresent === "" ? undefined : bePresent === "true";

const formatRootId = (rootId: string): string | undefined =>
  rootId === "" ? undefined : rootId;

const formatPercentage = (value: number, decimal?: boolean): string => {
  const formatter = new Intl.NumberFormat("en-IN", {
    maximumSignificantDigits: decimal === undefined || !decimal ? undefined : 1,
    style: "percent",
  });

  return formatter.format(value);
};

const commitFormatter = (value: string): string =>
  value.slice(0, COMMIT_LENGTH);

const getCoverage = (toeLinesAttr: IToeLinesAttr): number =>
  toeLinesAttr.loc === 0 ? 1 : toeLinesAttr.attackedLines / toeLinesAttr.loc;

const getDaysToAttack = (toeLinesAttr: IToeLinesAttr): number => {
  if (
    _.isNull(toeLinesAttr.attackedAt) ||
    _.isEmpty(toeLinesAttr.attackedAt) ||
    new Date(toeLinesAttr.modifiedDate) > new Date(toeLinesAttr.attackedAt)
  ) {
    if (toeLinesAttr.bePresent) {
      return Math.floor(
        (new Date().getTime() - new Date(toeLinesAttr.modifiedDate).getTime()) /
          (1000 * 3600 * 24)
      );
    }

    return Math.floor(
      (new Date(toeLinesAttr.bePresentUntil ?? "").getTime() -
        new Date(toeLinesAttr.modifiedDate).getTime()) /
        (1000 * 3600 * 24)
    );
  }

  return Math.floor(
    (new Date(toeLinesAttr.attackedAt).getTime() -
      new Date(toeLinesAttr.modifiedDate).getTime()) /
      (1000 * 3600 * 24)
  );
};

const getExtension = (toeLinesAttr: IToeLinesAttr): string => {
  const lastPointindex = toeLinesAttr.filename.lastIndexOf(".");
  const lastSlashIndex = toeLinesAttr.filename.lastIndexOf("/");
  if (lastPointindex === -1 || lastSlashIndex > lastPointindex) {
    return NOEXTENSION;
  }

  return toeLinesAttr.filename.slice(lastPointindex + 1);
};

const formatOptionalDate: (date: string | null) => Date | undefined = (
  date: string | null
): Date | undefined =>
  _.isNull(date) || _.isEmpty(date) ? undefined : new Date(date);

const formatToeLines: (toeLinesEdges: IToeLinesEdge[]) => IToeLinesData[] = (
  toeLinesEdges: IToeLinesEdge[]
): IToeLinesData[] =>
  toeLinesEdges.map(
    ({ node }): IToeLinesData => ({
      ...node,
      attackedAt: formatOptionalDate(node.attackedAt),
      bePresentUntil: formatOptionalDate(node.bePresentUntil),
      coverage: getCoverage(node),
      daysToAttack: getDaysToAttack(node),
      extension: getExtension(node),
      firstAttackAt: formatOptionalDate(node.firstAttackAt),
      lastCommit: commitFormatter(node.lastCommit),
      modifiedDate: formatOptionalDate(node.modifiedDate),
      rootId: node.root.id,
      rootNickname: node.root.nickname,
      seenAt: formatOptionalDate(node.seenAt),
    })
  );

const formatLinesFilter: (state: string) => string[] | string = (
  state: string
): string[] | string => {
  const linesParameters: Record<string, string[] | string> = {
    attackedAt: ["fromAttackedAt", "toAttackedAt"],
    attackedBy: "attackedBy",
    attackedLines: ["minAttackedLines", "maxAttackedLines"],
    bePresent: "bePresent",
    bePresentUntil: ["fromBePresentUntil", "toBePresentUntil"],
    comments: "comments",
    filename: "filename",
    firstAttackAt: ["fromFirstAttackAt", "toFirstAttackAt"],
    hasVulnerabilities: "hasVulnerabilities",
    lastAuthor: "lastAuthor",
    lastCommit: "lastCommit",
    loc: ["minLoc", "maxLoc"],
    modifiedDate: ["fromModifiedDate", "toModifiedDate"],
    seenAt: ["fromSeenAt", "toSeenAt"],
    sortsRiskLevel: ["minSortsRiskLevel", "maxSortsRiskLevel"],
  };

  return linesParameters[state];
};

const unformatFilterValues: (
  value: IFilter<IToeLinesData>
) => Record<string, unknown> = (
  value: IFilter<IToeLinesData>
): Record<string, unknown> => {
  const unformat = (): Record<string, unknown> => {
    const titleFormat = formatLinesFilter(value.id);

    if (typeof titleFormat === "string")
      return _.isUndefined(value.value)
        ? { [titleFormat]: undefined }
        : { [titleFormat]: value.value };

    return {
      [titleFormat[0]]: value.rangeValues?.[0],
      [titleFormat[1]]: value.rangeValues?.[1],
    };
  };

  return unformat();
};

export {
  formatBePresent,
  formatPercentage,
  formatRootId,
  formatToeLines,
  getFilteredData,
  getToeLinesIndex,
  onSelectSeveralToeLinesHelper,
  unformatFilterValues,
};
