/* eslint-disable complexity */

import { useApolloClient, useMutation, useQuery } from "@apollo/client";
import type { ApolloError, FetchResult } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type {
  ColumnDef,
  SortingState,
  VisibilityState,
} from "@tanstack/react-table";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { ActionButtons } from "./ActionButtons";
import { editableAttackedLinesFormatter } from "./formatters/editableAttackedLinesFormatter";
import { HandleAdditionModal } from "./HandleAdditionModal";
import { HandleEditionModal } from "./HandleEditionModal";
import { SortsSuggestionsModal } from "./SortsSuggestionsModal";
import { SortsSuggestionsButton } from "./styles";
import { formatBePresent, formatPercentage, formatRootId } from "./utils";

import type { IFilter } from "components/Filter";
import { Filters, useFilters } from "components/Filter";
import { Table } from "components/Table";
import { filterDate } from "components/Table/filters/filterFunctions/filterDate";
import type { ICellHelper } from "components/Table/types";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter";
import {
  GET_TOE_LINES,
  VERIFY_TOE_LINES,
} from "scenes/Dashboard/containers/GroupToeLinesView/queries";
import type {
  IGroupToeLinesViewProps,
  ISortsSuggestionAttr,
  IToeLinesAttr,
  IToeLinesConnection,
  IToeLinesData,
  IToeLinesEdge,
  IVerifyToeLinesResultAttr,
} from "scenes/Dashboard/containers/GroupToeLinesView/types";
import { authzPermissionsContext } from "utils/authz/config";
import { getErrors } from "utils/helpers";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const NOEXTENSION = ".no.extension.";

const GroupToeLinesView: React.FC<IGroupToeLinesViewProps> = ({
  isInternal,
}: IGroupToeLinesViewProps): JSX.Element => {
  const { t } = useTranslation();
  const client = useApolloClient();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateAttackedLines: boolean = permissions.can(
    "api_mutations_update_toe_lines_attacked_lines_mutate"
  );
  const canGetAttackedAt: boolean = permissions.can(
    "api_resolvers_toe_lines_attacked_at_resolve"
  );
  const canGetAttackedBy: boolean = permissions.can(
    "api_resolvers_toe_lines_attacked_by_resolve"
  );
  const canGetAttackedLines: boolean = permissions.can(
    "api_resolvers_toe_lines_attacked_lines_resolve"
  );
  const canGetBePresentUntil: boolean = permissions.can(
    "api_resolvers_toe_lines_be_present_until_resolve"
  );
  const canGetComments: boolean = permissions.can(
    "api_resolvers_toe_lines_comments_resolve"
  );
  const canGetFirstAttackAt: boolean = permissions.can(
    "api_resolvers_toe_lines_first_attack_at_resolve"
  );
  const canSeeCoverage: boolean = permissions.can("see_toe_lines_coverage");
  const canSeeDaysToAttack: boolean = permissions.can(
    "see_toe_lines_days_to_attack"
  );

  const { groupName } = useParams<{ groupName: string }>();

  const [isAdding, setIsAdding] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [isVerifying, setIsVerifying] = useState(false);
  const [selectedToeLinesDatas, setSelectedToeLinesDatas] = useState<
    IToeLinesData[]
  >([]);
  const [isSortsSuggestionsModalOpen, setIsSortsSuggestionsModalOpen] =
    useState(false);
  const [
    selectedToeLinesSortsSuggestions,
    setSelectedToeLinesSortsSuggestions,
  ] = useState<ISortsSuggestionAttr[]>();
  const closeSortsSuggestionsModal: () => void = useCallback((): void => {
    setIsSortsSuggestionsModalOpen(false);
  }, []);

  const [columnVisibility, setColumnVisibility] =
    useStoredState<VisibilityState>(
      "tblToeLines-visibilityState",
      {
        attackedBy: false,
        bePresent: false,
        bePresentUntil: false,
        daysToAttack: false,
        filename: false,
        firstAttackAt: false,
        lastAuthor: false,
        seenAt: false,
        sortsRiskLevel: false,
        sortsSuggestions: false,
      },
      localStorage
    );
  const [sorting, setSorting] = useStoredState<SortingState>(
    "tblToeLines-sortingState",
    []
  );

  function commitFormatter(value: string): string {
    const COMMIT_LENGTH: number = 7;

    return value.slice(0, COMMIT_LENGTH);
  }

  const formatDate: (date: Date | undefined) => string = (
    date: Date | undefined
  ): string => {
    if (_.isUndefined(date)) {
      return "";
    }

    // eslint-disable-next-line new-cap
    return Intl.DateTimeFormat("fr-CA", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    }).format(date);
  };
  const formatBoolean = (value: boolean): string =>
    value ? t("group.toe.lines.yes") : t("group.toe.lines.no");
  const formatHasVulnerabilityStatus = (value: boolean): string =>
    value ? t("group.toe.lines.vulnerable") : t("group.toe.lines.safe");
  const formatSortsRiskLevel = (sortsRiskLevel: number): string =>
    sortsRiskLevel >= 0 ? `${sortsRiskLevel.toString()} %` : "n/a";

  const formatSortsSuggestions = (
    sortsSuggestions: ISortsSuggestionAttr[] | null
  ): JSX.Element => {
    const value =
      _.isNil(sortsSuggestions) || sortsSuggestions.length === 0
        ? "None"
        : `${sortsSuggestions.length} available`;

    return (
      <SortsSuggestionsButton
        isNone={value === "None"}
        // eslint-disable-next-line react/jsx-no-bind
        onClick={(): void => {
          if (!_.isNil(sortsSuggestions)) {
            setSelectedToeLinesSortsSuggestions(sortsSuggestions);
            setIsSortsSuggestionsModalOpen(true);
          }
        }}
      >
        {value}
      </SortsSuggestionsButton>
    );
  };

  // // GraphQL operations
  const [handleVerifyToeLines] = useMutation<IVerifyToeLinesResultAttr>(
    VERIFY_TOE_LINES,
    {
      onError: (errors: ApolloError): void => {
        errors.graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - The toe lines has been updated by another operation":
              msgError(t("group.toe.lines.editModal.alerts.alreadyUpdate"));
              break;
            case "Exception - The attacked lines must be between 0 and the loc (lines of code)":
              msgError(
                t(
                  "group.toe.lines.editModal.alerts.invalidAttackedLinesBetween"
                )
              );
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning("An error occurred verifying a toe lines", error);
          }
        });
      },
    }
  );
  const getToeLinesVariables = {
    canGetAttackedAt,
    canGetAttackedBy,
    canGetAttackedLines,
    canGetBePresentUntil,
    canGetComments,
    canGetFirstAttackAt,
    groupName,
    rootId: formatRootId(""),
  };
  const { data, fetchMore, refetch } = useQuery<{
    group: {
      toeLines: IToeLinesConnection;
    };
  }>(GET_TOE_LINES, {
    fetchPolicy: "network-only",
    nextFetchPolicy: "cache-first",
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load group toe lines", error);
      });
    },
    variables: {
      ...getToeLinesVariables,
      bePresent: formatBePresent(""),
      first: 150,
    },
  });
  const pageInfo =
    data === undefined ? undefined : data.group.toeLines.pageInfo;
  const toeLinesEdges: IToeLinesEdge[] =
    data === undefined ? [] : data.group.toeLines.edges;
  const getCoverage = (toeLinesAttr: IToeLinesAttr): number =>
    toeLinesAttr.loc === 0 ? 1 : toeLinesAttr.attackedLines / toeLinesAttr.loc;
  const getDaysToAttack = (toeLinesAttr: IToeLinesAttr): number =>
    _.isNull(toeLinesAttr.attackedAt) ||
    _.isEmpty(toeLinesAttr.attackedAt) ||
    new Date(toeLinesAttr.modifiedDate) > new Date(toeLinesAttr.attackedAt)
      ? toeLinesAttr.bePresent
        ? Math.floor(
            (new Date().getTime() -
              new Date(toeLinesAttr.modifiedDate).getTime()) /
              (1000 * 3600 * 24)
          )
        : Math.floor(
            (new Date(toeLinesAttr.bePresentUntil ?? "").getTime() -
              new Date(toeLinesAttr.modifiedDate).getTime()) /
              (1000 * 3600 * 24)
          )
      : Math.floor(
          (new Date(toeLinesAttr.attackedAt).getTime() -
            new Date(toeLinesAttr.modifiedDate).getTime()) /
            (1000 * 3600 * 24)
        );
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
  const toeLines: IToeLinesData[] = toeLinesEdges.map(
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

  const handleUpdateAttackedLines: (
    rootId: string,
    filename: string,
    attackedLines: number
  ) => Promise<void> = async (
    rootId: string,
    filename: string,
    attackedLines: number
  ): Promise<void> => {
    const result = await handleVerifyToeLines({
      variables: {
        ...getToeLinesVariables,
        attackedLines,
        filename,
        groupName,
        rootId,
        shouldGetNewToeLines: true,
      },
    });

    if (
      !_.isNil(result.data) &&
      result.data.updateToeLinesAttackedLines.success
    ) {
      msgSuccess(
        t("group.toe.lines.alerts.verifyToeLines.success"),
        t("groupAlerts.updatedTitle")
      );
      const updatedToeLines = result.data.updateToeLinesAttackedLines.toeLines;

      if (!_.isUndefined(updatedToeLines)) {
        client.writeQuery({
          data: {
            ...data,
            group: {
              ...data?.group,
              toeLines: {
                ...data?.group.toeLines,
                edges: data?.group.toeLines.edges.map(
                  (value: IToeLinesEdge): IToeLinesEdge =>
                    value.node.root.id === rootId &&
                    value.node.filename === filename
                      ? {
                          node: updatedToeLines,
                        }
                      : { node: value.node }
                ),
              },
            },
          },
          query: GET_TOE_LINES,
          variables: {
            ...getToeLinesVariables,
            bePresent: formatBePresent(""),
            first: 150,
          },
        });
      }
    }
  };

  const columns: ColumnDef<IToeLinesData>[] = [
    {
      accessorKey: "rootNickname",
      header: t("group.toe.lines.root"),
    },
    {
      accessorKey: "filename",
      header: t("group.toe.lines.filename"),
    },
    {
      accessorKey: "loc",
      header: t("group.toe.lines.loc"),
    },
    {
      accessorFn: (row: IToeLinesData): string =>
        formatHasVulnerabilityStatus(row.hasVulnerabilities),
      cell: (cell: ICellHelper<IToeLinesData>): JSX.Element =>
        statusFormatter(cell.getValue()),
      header: t("group.toe.lines.status"),
      id: "hasVulnerabilities",
    },
    {
      accessorKey: "modifiedDate",
      cell: (cell: ICellHelper<IToeLinesData>): string =>
        formatDate(cell.getValue()),
      filterFn: filterDate,
      header: t("group.toe.lines.modifiedDate"),
    },
    {
      accessorKey: "lastCommit",
      header: t("group.toe.lines.lastCommit"),
    },
    {
      accessorKey: "lastAuthor",
      header: t("group.toe.lines.lastAuthor"),
    },
    {
      accessorKey: "seenAt",
      cell: (cell: ICellHelper<IToeLinesData>): string =>
        formatDate(cell.getValue()),
      filterFn: filterDate,
      header: t("group.toe.lines.seenAt"),
    },
    {
      accessorKey: "sortsRiskLevel",
      cell: (cell: ICellHelper<IToeLinesData>): string =>
        formatSortsRiskLevel(cell.getValue()),
      header: t("group.toe.lines.sortsRiskLevel"),
    },
    {
      accessorFn: (row: IToeLinesData): string => formatBoolean(row.bePresent),
      header: t("group.toe.lines.bePresent"),
      id: "bePresent",
    },
    {
      accessorFn: (row): number => row.coverage * 100,
      cell: (cell: ICellHelper<IToeLinesData>): string =>
        formatPercentage(cell.row.original.coverage),
      header: t("group.toe.lines.coverage"),
      id: "coverage",
    },
    {
      accessorKey: "attackedLines",
      cell: (cell: ICellHelper<IToeLinesData>): JSX.Element | string =>
        editableAttackedLinesFormatter(
          canUpdateAttackedLines,
          handleUpdateAttackedLines,
          cell.row.original
        ),
      header: t("group.toe.lines.attackedLines"),
      id: "attackedLines",
    },
    {
      accessorKey: "daysToAttack",
      header: t("group.toe.lines.daysToAttack"),
      id: "daysToAttack",
    },
    {
      accessorKey: "attackedAt",
      cell: (cell: ICellHelper<IToeLinesData>): string =>
        formatDate(cell.getValue()),
      filterFn: filterDate,
      header: t("group.toe.lines.attackedAt"),
      id: "attackedAt",
    },
    {
      accessorKey: "attackedBy",
      header: t("group.toe.lines.attackedBy"),
      id: "attackedBy",
      meta: { filterType: "select" },
    },
    {
      accessorKey: "firstAttackAt",
      cell: (cell: ICellHelper<IToeLinesData>): string =>
        formatDate(cell.getValue()),
      filterFn: filterDate,
      header: t("group.toe.lines.firstAttackAt"),
      id: "firstAttackAt",
    },
    {
      accessorKey: "comments",
      header: t("group.toe.lines.comments"),
      id: "comments",
    },
    {
      accessorKey: "sortsSuggestions",
      cell: (cell: ICellHelper<IToeLinesData>): JSX.Element =>
        formatSortsSuggestions(cell.getValue()),
      header: t("group.toe.lines.sortsSuggestions"),
      id: "sortsSuggestions",
    },
    {
      accessorKey: "bePresentUntil",
      cell: (cell: ICellHelper<IToeLinesData>): string =>
        formatDate(cell.getValue()),
      filterFn: filterDate,
      header: t("group.toe.lines.bePresentUntil"),
      id: "bePresentUntil",
    },
  ];

  const baseFilters: IFilter<IToeLinesData>[] = [
    {
      id: "rootNickname",
      key: "rootNickname",
      label: t("group.toe.lines.root"),
      selectOptions: (lines: IToeLinesData[]): string[] =>
        [
          ...new Set(lines.map((datapoint): string => datapoint.rootNickname)),
        ].filter(Boolean),
      type: "select",
    },
    {
      id: "filename",
      key: "filename",
      label: t("group.toe.lines.filename"),
      type: "text",
    },
    {
      id: "loc",
      key: "loc",
      label: t("group.toe.lines.loc"),
      type: "numberRange",
    },
    {
      id: "hasVulnerabilities",
      key: "hasVulnerabilities",
      label: t("group.toe.lines.status"),
      selectOptions: [
        { header: formatHasVulnerabilityStatus(true), value: "true" },
        { header: formatHasVulnerabilityStatus(false), value: "false" },
      ],
      type: "select",
    },
    {
      id: "modifiedDate",
      key: "modifiedDate",
      label: t("group.toe.lines.modifiedDate"),
      type: "dateRange",
    },
    {
      id: "lastCommit",
      key: "lastCommit",
      label: t("group.toe.lines.lastCommit"),
      type: "text",
    },
    {
      id: "lastAuthor",
      key: "lastAuthor",
      label: t("group.toe.lines.lastAuthor"),
      type: "text",
    },
    {
      id: "seenAt",
      key: "seenAt",
      label: t("group.toe.lines.seenAt"),
      type: "dateRange",
    },
    {
      id: "sortsRiskLevel",
      key: "sortsRiskLevel",
      label: t("group.toe.lines.sortsRiskLevel"),
      type: "numberRange",
    },
    {
      id: "bePresent",
      key: "bePresent",
      label: t("group.toe.lines.bePresent"),
      selectOptions: [
        { header: formatBoolean(true), value: "true" },
        { header: formatBoolean(false), value: "false" },
      ],
      type: "select",
    },
    {
      id: "coverage",
      key: (arg0, _value, rangeValues): boolean => {
        if (_.isNil(rangeValues)) return true;
        const coverage = arg0.coverage * 100;
        const isHigher = _.isEmpty(rangeValues[0])
          ? true
          : coverage >= parseInt(rangeValues[0], 10);
        const isLower = _.isEmpty(rangeValues[1])
          ? true
          : coverage <= parseInt(rangeValues[1], 10);

        return isHigher && isLower;
      },
      label: t("group.toe.lines.coverage"),
      type: "numberRange",
    },
    {
      id: "attackedLines",
      key: "attackedLines",
      label: t("group.toe.lines.attackedLines"),
      type: "text",
    },
    {
      id: "daysToAttack",
      key: "daysToAttack",
      label: t("group.toe.lines.daysToAttack"),
      type: "numberRange",
    },
    {
      id: "attackedAt",
      key: "attackedAt",
      label: t("group.toe.lines.attackedAt"),
      type: "dateRange",
    },
    {
      id: "attackedBy",
      key: "attackedBy",
      label: t("group.toe.lines.attackedBy"),
      selectOptions: (lines: IToeLinesData[]): string[] =>
        [
          ...new Set(lines.map((datapoint): string => datapoint.attackedBy)),
        ].filter(Boolean),
      type: "select",
    },
    {
      id: "firstAttackAt",
      key: "firstAttackAt",
      label: t("group.toe.lines.firstAttackAt"),
      type: "dateRange",
    },
    {
      id: "comments",
      key: "comments",
      label: t("group.toe.lines.comments"),
      type: "text",
    },
    {
      id: "sortsSuggestions",
      key: "sortsSuggestions",
      label: t("group.toe.lines.sortsSuggestions"),
      type: "text",
    },
    {
      id: "bePresentUntil",
      key: "bePresentUntil",
      label: t("group.toe.lines.bePresentUntil"),
      type: "dateRange",
    },
  ];

  const tablecolumns = columns.filter((column): boolean => {
    switch (column.id) {
      case "coverage":
        return isInternal && canSeeCoverage && canGetAttackedLines;
      case "attackedLines":
        return isInternal && canGetAttackedLines;
      case "daysToAttack":
        return isInternal && canSeeDaysToAttack && canGetAttackedAt;
      case "attackedAt":
        return isInternal && canGetAttackedAt;
      case "attackedBy":
        return isInternal && canGetAttackedBy;
      case "firstAttackAt":
        return isInternal && canGetFirstAttackAt;
      case "comments":
        return isInternal && canGetComments;
      case "sortsSuggestions":
        return isInternal;
      case "bePresentUntil":
        return isInternal && canGetBePresentUntil;
      default:
        return true;
    }
  });

  const tableFilters = baseFilters.filter((filter): boolean => {
    switch (filter.id) {
      case "coverage":
        return isInternal && canSeeCoverage && canGetAttackedLines;
      case "attackedLines":
        return isInternal && canGetAttackedLines;
      case "daysToAttack":
        return isInternal && canSeeDaysToAttack && canGetAttackedAt;
      case "attackedAt":
        return isInternal && canGetAttackedAt;
      case "attackedBy":
        return isInternal && canGetAttackedBy;
      case "firstAttackAt":
        return isInternal && canGetFirstAttackAt;
      case "comments":
        return isInternal && canGetComments;
      case "sortsSuggestions":
        return isInternal;
      case "bePresentUntil":
        return isInternal && canGetBePresentUntil;
      default:
        return true;
    }
  });

  const [filters, setFilters] =
    useState<IFilter<IToeLinesData>[]>(tableFilters);

  const filteredToeLines = useFilters(toeLines, filters);

  useEffect((): void => {
    if (!_.isUndefined(pageInfo)) {
      if (pageInfo.hasNextPage) {
        void fetchMore({
          variables: { after: pageInfo.endCursor, first: 1200 },
        });
      }
    }
  }, [pageInfo, fetchMore]);
  useEffect((): void => {
    setSelectedToeLinesDatas([]);
    void refetch();
  }, [refetch]);

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  function toggleAdd(): void {
    setIsAdding(!isAdding);
  }
  function toggleEdit(): void {
    setIsEditing(!isEditing);
  }

  const handleOnVerifyCompleted = (
    result: FetchResult<IVerifyToeLinesResultAttr>
  ): void => {
    if (
      !_.isNil(result.data) &&
      result.data.updateToeLinesAttackedLines.success
    ) {
      msgSuccess(
        t("group.toe.lines.alerts.verifyToeLines.success"),
        t("groupAlerts.updatedTitle")
      );
      void refetch();
      setSelectedToeLinesDatas([]);
    }
  };

  async function handleVerify(): Promise<void> {
    setIsVerifying(true);
    const results = await Promise.all(
      selectedToeLinesDatas.map(
        async (
          toeInputData: IToeLinesData
        ): Promise<FetchResult<IVerifyToeLinesResultAttr>> =>
          handleVerifyToeLines({
            variables: {
              ...getToeLinesVariables,
              filename: toeInputData.filename,
              groupName,
              rootId: toeInputData.rootId,
              shouldGetNewToeLines: false,
            },
          })
      )
    );
    const errors = getErrors<IVerifyToeLinesResultAttr>(results);

    if (!_.isEmpty(results) && _.isEmpty(errors)) {
      handleOnVerifyCompleted(results[0]);
    } else {
      void refetch();
    }
    setIsVerifying(false);
  }

  return (
    <React.StrictMode>
      <Table
        columnToggle={true}
        columnVisibilitySetter={setColumnVisibility}
        columnVisibilityState={columnVisibility}
        columns={tablecolumns}
        data={filteredToeLines}
        exportCsv={true}
        extraButtons={
          <ActionButtons
            areToeLinesDatasSelected={selectedToeLinesDatas.length > 0}
            isAdding={isAdding}
            isEditing={isEditing}
            isInternal={isInternal}
            isVerifying={isVerifying}
            onAdd={toggleAdd}
            onEdit={toggleEdit}
            onVerify={handleVerify}
          />
        }
        filters={
          <Filters
            dataset={toeLines}
            filters={filters}
            setFilters={setFilters}
          />
        }
        id={"tblToeLines"}
        rowSelectionSetter={
          isInternal && canUpdateAttackedLines
            ? setSelectedToeLinesDatas
            : undefined
        }
        rowSelectionState={selectedToeLinesDatas}
        sortingSetter={setSorting}
        sortingState={sorting}
      />
      <HandleAdditionModal
        groupName={groupName}
        handleCloseModal={toggleAdd}
        isAdding={isAdding}
        refetchData={refetch}
      />
      {isEditing ? (
        <HandleEditionModal
          groupName={groupName}
          handleCloseModal={toggleEdit}
          refetchData={refetch}
          selectedToeLinesDatas={selectedToeLinesDatas}
          setSelectedToeLinesDatas={setSelectedToeLinesDatas}
        />
      ) : undefined}
      <SortsSuggestionsModal
        closeSortsSuggestionsModal={closeSortsSuggestionsModal}
        isSortsSuggestionsOpen={isSortsSuggestionsModalOpen}
        selectedSortsSuggestions={selectedToeLinesSortsSuggestions}
      />
    </React.StrictMode>
  );
};

export { GroupToeLinesView };
