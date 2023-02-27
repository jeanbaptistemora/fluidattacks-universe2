/* eslint @typescript-eslint/no-unnecessary-condition:0 */
import { useLazyQuery, useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import {
  faArrowRight,
  faPlus,
  faTrashAlt,
} from "@fortawesome/free-solid-svg-icons";
import type {
  ColumnDef,
  Row,
  SortingState,
  VisibilityState,
} from "@tanstack/react-table";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, {
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import type { FormEvent } from "react";
import { useTranslation } from "react-i18next";
import { useHistory, useParams, useRouteMatch } from "react-router-dom";

import { renderDescription } from "./description";
import { assigneesFormatter } from "./formatters/assigneesFormatter";
import { locationsFormatter } from "./formatters/locationsFormatter";
import { severityFormatter } from "./formatters/severityFormatter";
import {
  ADD_FINDING_MUTATION,
  GET_GROUP_VULNERABILITIES,
  GET_ROOTS,
} from "./queries";
import type {
  IAddFindingMutationResult,
  IFindingSuggestionData,
  IGroupVulnerabilities,
  IRoot,
  IVulnerabilitiesResume,
  IVulnerability,
} from "./types";
import {
  formatFindings,
  formatState,
  getAreAllMutationValid,
  getFindingSuggestions,
  getResults,
  getRiskExposure,
  handleRemoveFindingsError,
} from "./utils";

import { REMOVE_FINDING_MUTATION } from "../../Finding-Content/queries";
import { formatPercentage } from "../ToeContent/GroupToeLinesView/utils";
import { Button } from "components/Button";
import { Empty } from "components/Empty";
import type { IFilter, IPermanentData } from "components/Filter";
import { Filters, useFilters } from "components/Filter";
import { Label, Select, TextArea } from "components/Input";
import { Modal, ModalConfirm } from "components/Modal";
import { Table } from "components/Table";
import { newTagFormatter } from "components/Table/formatters/newTagFormatter";
import type { ICellHelper } from "components/Table/types";
import { Tooltip } from "components/Tooltip";
import { searchingFindings } from "resources";
import { ExpertButton } from "scenes/Dashboard/components/ExpertButton";
import { RiskExposureTour } from "scenes/Dashboard/components/RiskExposureTour/RiskExposureTour";
import { WelcomeModal } from "scenes/Dashboard/components/WelcomeModal";
import { GET_FINDINGS } from "scenes/Dashboard/containers/Group-Content/GroupFindingsView/queries";
import { ReportsModal } from "scenes/Dashboard/containers/Group-Content/GroupFindingsView/reportsModal";
import type {
  IFindingAttr,
  IGroupFindingsAttr,
} from "scenes/Dashboard/containers/Group-Content/GroupFindingsView/types";
import { vulnerabilitiesContext } from "scenes/Dashboard/group/context";
import type { IVulnerabilitiesContext } from "scenes/Dashboard/group/types";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { FormikAutocompleteText } from "utils/forms/fields";
import { useDebouncedCallback, useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { composeValidators, required } from "utils/validations";

const GroupFindingsView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const {
    openVulnerabilities,
    setOpenVulnerabilities,
  }: IVulnerabilitiesContext = useContext(vulnerabilitiesContext);
  const { push } = useHistory();
  const { url } = useRouteMatch();
  const { t } = useTranslation();

  // State management
  const [isReportsModalOpen, setIsReportsModalOpen] = useState(false);
  const [isAddFindingModalOpen, setIsAddFindingModalOpen] = useState(false);
  const [addFindingInitialValues, setAddFindingInitialValues] = useState({
    description: "",
    recommendation: "",
    title: "",
  });
  const [suggestions, setSuggestions] = useState<
    IFindingSuggestionData[] | undefined
  >(undefined);
  const [filters, setFilters] = useState<IFilter<IFindingAttr>[]>([
    {
      id: "lastVulnerability",
      key: "lastVulnerability",
      label: "Last Report",
      type: "number",
    },
    {
      id: "title",
      key: "title",
      label: "Type",
      selectOptions: (findings: IFindingAttr[]): string[] =>
        [
          ...new Set(findings.map((finding): string => finding.title ?? "")),
        ].filter(Boolean),
      type: "select",
    },
    {
      id: "state",
      key: "status",
      label: "Status",
      selectOptions: [
        {
          header: t("searchFindings.header.status.stateLabel.open"),
          value: "VULNERABLE",
        },
        {
          header: t("searchFindings.header.status.stateLabel.closed"),
          value: "SAFE",
        },
      ],
      type: "select",
    },
    {
      id: "treatment",
      key: (finding: IFindingAttr, value?: string): boolean => {
        if (value === "" || value === undefined) return true;

        return (
          finding.treatmentSummary[
            value as keyof typeof finding.treatmentSummary
          ] > 0
        );
      },
      label: t("searchFindings.tabVuln.vulnTable.treatment"),
      selectOptions: [
        {
          header: t("searchFindings.tabDescription.treatment.new"),
          value: "untreated",
        },
        {
          header: t("searchFindings.tabDescription.treatment.inProgress"),
          value: "inProgress",
        },
        {
          header: t("searchFindings.tabDescription.treatment.accepted"),
          value: "accepted",
        },
        {
          header: t(
            "searchFindings.tabDescription.treatment.acceptedUndefined"
          ),
          value: "acceptedUndefined",
        },
      ],
      type: "select",
    },
    {
      id: "severityScore",
      key: "severityScore",
      label: "Severity",
      type: "numberRange",
    },
    {
      id: "age",
      key: "age",
      label: "Age",
      type: "number",
    },
    {
      id: "reattack",
      key: "reattack",
      label: "Reattack",
      selectOptions: ["-", "Pending"],
      type: "select",
    },
    {
      id: "releaseDate",
      key: "releaseDate",
      label: "Release Date",
      type: "dateRange",
    },
  ]);
  const [filterVal, setFilterVal] = useStoredState<IPermanentData[]>(
    "tblFindFilters",
    [
      { id: "lastVulnerability", value: "" },
      { id: "title", value: "" },
      { id: "state", value: "" },
      { id: "treatment", value: "" },
      { id: "severityScore", rangeValues: ["", ""] },
      { id: "age", value: "" },
      { id: "locationsInfo", value: "" },
      { id: "reattack", value: "" },
      { id: "releaseDate", rangeValues: ["", ""] },
    ],
    localStorage
  );
  const [columnVisibility, setColumnVisibility] =
    useStoredState<VisibilityState>("tblFindings-visibilityState", {
      Assignees: false,
      Locations: false,
      Treatment: false,
      age: false,
      closingPercentage: false,
      description: false,
      reattack: false,
      releaseDate: false,
    });
  const [sorting, setSorting] = useStoredState<SortingState>(
    "tblFindings-sortingState",
    []
  );
  const openAddFindingModal: () => void =
    useCallback(async (): Promise<void> => {
      setIsAddFindingModalOpen(true);
      if (_.isUndefined(suggestions)) {
        const findingSuggestions: IFindingSuggestionData[] =
          await getFindingSuggestions().catch(
            (error: Error): IFindingSuggestionData[] => {
              Logger.error(
                "An error occurred getting finding suggestions",
                error
              );

              return [];
            }
          );
        setSuggestions(findingSuggestions);
      }
    }, [suggestions]);
  const closeAddFindingModal: () => void = useCallback((): void => {
    setIsAddFindingModalOpen(false);
  }, []);
  const openReportsModal: () => void = useCallback((): void => {
    setIsReportsModalOpen(true);
  }, []);
  const closeReportsModal: () => void = useCallback((): void => {
    setIsReportsModalOpen(false);
  }, []);

  const [isRunning, setIsRunning] = useState(false);
  const [selectedFindings, setSelectedFindings] = useState<IFindingAttr[]>([]);

  const [findingVulnerabilities, setFindingVulnerabilities] = useState<
    Record<string, IVulnerabilitiesResume>
  >({});

  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const openDeleteModal: () => void = useCallback((): void => {
    setIsDeleteModalOpen(true);
  }, []);
  const closeDeleteModal: () => void = useCallback((): void => {
    setIsDeleteModalOpen(false);
  }, []);

  const goToFinding = useCallback(
    (rowInfo: Row<IFindingAttr>): ((event: FormEvent) => void) => {
      return (event: FormEvent): void => {
        push(`${url}/${rowInfo.original.id}/locations`);
        event.preventDefault();
      };
    },
    [push, url]
  );

  const handleQryErrors: (error: ApolloError) => void = useCallback(
    ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading group data", error);
      });
    },
    [t]
  );

  const { data, loading, refetch } = useQuery<IGroupFindingsAttr>(
    GET_FINDINGS,
    {
      fetchPolicy: "cache-first",
      onError: handleQryErrors,
      variables: { groupName },
    }
  );

  const [getVuln, { data: vulnData }] = useLazyQuery<IGroupVulnerabilities>(
    GET_GROUP_VULNERABILITIES,
    {
      fetchPolicy: "cache-and-network",
      nextFetchPolicy: "cache-first",
    }
  );

  const { data: rootsData } = useQuery<{ group: { roots: IRoot[] } }>(
    GET_ROOTS,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          Logger.error("Couldn't load roots", error);
        });
      },
      variables: { groupName },
    }
  );

  useEffect((): void => {
    if (!_.isUndefined(data) && !_.isUndefined(setOpenVulnerabilities)) {
      const newValue = data.group.findings.reduce(
        (previousValue: number, find: IFindingAttr): number =>
          previousValue + find.openVulnerabilities,
        0
      );
      if (openVulnerabilities !== newValue) {
        setOpenVulnerabilities(newValue);
      }
    }
  }, [data, openVulnerabilities, setOpenVulnerabilities]);

  useEffect((): void => {
    if (!_.isUndefined(vulnData)) {
      const { edges } = vulnData.group.vulnerabilities;

      edges
        .map((edge): IVulnerability => edge.node)
        .forEach((vulnerability): void => {
          setFindingVulnerabilities(
            (
              prevState: Record<string, IVulnerabilitiesResume>
            ): Record<string, IVulnerabilitiesResume> => {
              const current = prevState[vulnerability.findingId] ?? {
                treatmentAssignmentEmails: new Set(),
                wheres: "",
              };
              const wheres =
                current.wheres === ""
                  ? vulnerability.where
                  : [current.wheres, vulnerability.where].join(", ");

              const treatmentAssignmentEmails = new Set(
                [
                  ...current.treatmentAssignmentEmails,
                  vulnerability.state === "VULNERABLE"
                    ? (vulnerability.treatmentAssigned as string)
                    : "",
                ].filter(Boolean)
              );

              return {
                ...prevState,
                [vulnerability.findingId]: {
                  treatmentAssignmentEmails,
                  wheres,
                },
              };
            }
          );
        });
    }
  }, [vulnData]);

  const hasMachine = data?.group.hasMachine ?? false;
  const filledGroupInfo =
    !_.isEmpty(data?.group.description) &&
    !_.isEmpty(data?.group.businessId) &&
    !_.isEmpty(data?.group.businessName);

  const activeRoots: IRoot[] =
    rootsData === undefined
      ? []
      : [
          ...rootsData.group.roots.filter(
            (root): boolean => root.state === "ACTIVE"
          ),
        ];

  const findings: IFindingAttr[] = useMemo(
    (): IFindingAttr[] =>
      data === undefined
        ? []
        : formatFindings(data.group.findings, findingVulnerabilities),
    [data, findingVulnerabilities]
  );

  const orderedFindings: IFindingAttr[] = _.orderBy(
    findings,
    ["status", "severityScore"],
    ["desc", "desc"]
  );

  const filteredFindings = useFilters(orderedFindings, filters);

  const groupCVSSF = findings
    .filter((find): boolean => find.status === "VULNERABLE")
    .reduce(
      (sum, finding): number => sum + 4 ** (finding.severityScore - 4),
      0
    );

  const tableColumns: ColumnDef<IFindingAttr>[] = [
    {
      accessorKey: "title",
      cell: (cell: ICellHelper<IFindingAttr>): JSX.Element | string => {
        const finding: IFindingAttr = cell.row.original;

        return finding.lastVulnerability <= 7 && finding.openVulnerabilities > 0
          ? newTagFormatter(finding.title)
          : finding.title;
      },
      header: "Type",
    },
    {
      accessorKey: "status",
      cell: (cell: ICellHelper<IFindingAttr>): JSX.Element =>
        formatState(cell.getValue()),
      header: "Status",
    },
    {
      accessorKey: "severityScore",
      cell: (cell: ICellHelper<IFindingAttr>): JSX.Element =>
        severityFormatter(cell.getValue()),
      header: "Severity",
    },
    {
      accessorFn: (row: IFindingAttr): number => {
        return getRiskExposure(row.status, row.severityScore, groupCVSSF);
      },
      cell: (cell: ICellHelper<IFindingAttr>): string =>
        formatPercentage(cell.getValue(), true),
      header: "% Risk Exposure",
      id: "riskExposureColumn",
    },
    {
      accessorKey: "openVulnerabilities",
      header: "Open Vulnerabilities",
    },
    {
      accessorKey: "lastVulnerability",
      cell: (cell: ICellHelper<IFindingAttr>): string =>
        t("group.findings.description.value", { count: cell.getValue() }),
      header: "Last report",
    },
    {
      accessorKey: "age",
      header: "Age",
    },
    {
      accessorKey: "closingPercentage",
      cell: (cell: ICellHelper<IFindingAttr>): string =>
        formatPercentage(cell.getValue()),
      header: t("group.findings.closingPercentage"),
    },
    {
      accessorFn: (row: IFindingAttr): string | undefined =>
        row.locationsInfo.locations,
      cell: (cell: ICellHelper<IFindingAttr>): JSX.Element =>
        locationsFormatter(cell.row.original.locationsInfo),
      header: "Locations",
    },
    {
      accessorKey: "reattack",
      header: "Reattack",
    },
    {
      accessorFn: (row: IFindingAttr): string[] =>
        Array.from(row.locationsInfo.treatmentAssignmentEmails.values()),
      cell: (cell: ICellHelper<IFindingAttr>): JSX.Element =>
        assigneesFormatter(
          Array.from(
            cell.row.original.locationsInfo.treatmentAssignmentEmails.values()
          )
        ),
      header: "Assignees",
    },
    {
      accessorKey: "releaseDate",
      header: "Release Date",
    },
    {
      accessorFn: (row: IFindingAttr): string[] => {
        const treatment = row.treatmentSummary;
        const treatmentNew = treatment.untreated > 0 ? "Untreated" : "";
        const treatmentAccUndef =
          treatment.acceptedUndefined > 0 ? "Permanently Accepted" : "";
        const treatmentInProgress =
          treatment.inProgress > 0 ? "In Progress" : "";
        const treatmentAccepted =
          treatment.accepted > 0 ? "Temporarily Accepted" : "";

        return [
          treatmentNew,
          treatmentInProgress,
          treatmentAccepted,
          treatmentAccUndef,
        ].filter(Boolean);
      },
      cell: (cell: ICellHelper<IFindingAttr>): string => {
        const treatment = cell.row.original.treatmentSummary;

        return `Untreated: ${treatment.untreated}, In Progress: ${treatment.inProgress},
        Temporarily Accepted:  ${treatment.accepted}, Permamently Accepted:
        ${treatment.acceptedUndefined}`;
      },
      header: "Treatment",
    },
    {
      accessorKey: "description",
      header: "Description",
    },
  ];

  const typesArray = findings.map((find: IFindingAttr): string[] => [
    find.title,
    find.title,
  ]);
  const typesOptions = Object.fromEntries(
    _.sortBy(typesArray, (arr): string => arr[0])
  );

  const [addFinding, { loading: addingFinding }] = useMutation<
    IAddFindingMutationResult,
    Omit<IFindingSuggestionData, "code"> | { groupName: string }
  >(ADD_FINDING_MUTATION, {
    onCompleted: async (result: IAddFindingMutationResult): Promise<void> => {
      if (result.addFinding.success) {
        msgSuccess(
          t("group.findings.addModal.alerts.addedFinding"),
          t("groupAlerts.titleSuccess")
        );
        await refetch();
        setIsAddFindingModalOpen(false);
      }
    },
    onError: (errors: ApolloError): void => {
      errors.graphQLErrors.forEach((error: GraphQLError): void => {
        if (error.message) {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred adding finding", error);
        }
      });
    },
  });

  const handleAdd = useCallback(
    async ({ title }: { title: string }): Promise<void> => {
      const [matchingSuggestion]: IFindingSuggestionData[] = _.isUndefined(
        suggestions
      )
        ? []
        : suggestions.filter(
            (suggestion: IFindingSuggestionData): boolean =>
              `${suggestion.code}. ${suggestion.title}` === title
          );
      const draftData = _.omit(matchingSuggestion, ["code"]);
      await addFinding({
        variables: {
          ...draftData,
          groupName,
          title,
        },
      });
    },
    [addFinding, groupName, suggestions]
  );

  const [removeFinding, { loading: deleting }] = useMutation(
    REMOVE_FINDING_MUTATION,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred deleting finding", error);
        });
      },
    }
  );

  const validMutationsHelper = useCallback(
    (handleCloseModal: () => void, areAllMutationValid: boolean[]): void => {
      if (areAllMutationValid.every(Boolean)) {
        msgSuccess(
          t("group.findings.deleteModal.alerts.vulnerabilitiesDeleted"),
          t("group.drafts.titleSuccess")
        );
        void refetch();
        handleCloseModal();
      }
    },
    [refetch, t]
  );

  const handleRemoveFinding = useCallback(
    async (justification: unknown): Promise<void> => {
      setIsRunning(true);
      if (selectedFindings.length === 0) {
        msgError(t("searchFindings.tabResources.noSelection"));
        setIsRunning(false);
      } else {
        try {
          const results = await getResults(
            removeFinding,
            selectedFindings,
            justification
          );
          const areAllMutationValid = getAreAllMutationValid(results);
          validMutationsHelper(closeDeleteModal, areAllMutationValid);
        } catch (updateError: unknown) {
          handleRemoveFindingsError(updateError);
        } finally {
          setIsRunning(false);
        }
      }
    },
    [closeDeleteModal, removeFinding, selectedFindings, t, validMutationsHelper]
  );

  const handleDelete = useCallback(
    async (values: Record<string, unknown>): Promise<void> => {
      await handleRemoveFinding(values.justification);
    },
    [handleRemoveFinding]
  );

  const handleSearch = useDebouncedCallback((root: string): void => {
    getVuln({ variables: { first: 1200, groupName, root } });
  }, 500);

  const handleRowExpand = useCallback((row: Row<IFindingAttr>): JSX.Element => {
    return renderDescription(row.original);
  }, []);

  const getFindingMatchingSuggestion = useCallback(
    (findingName: string): IFindingSuggestionData | undefined => {
      const [matchingSuggestion]: IFindingSuggestionData[] = _.isUndefined(
        suggestions
      )
        ? []
        : suggestions.filter(
            (suggestion: IFindingSuggestionData): boolean =>
              `${suggestion.code}. ${suggestion.title}` === findingName
          );

      return matchingSuggestion;
    },
    [suggestions]
  );

  const handleAddFindingTitleChange = useCallback(
    ({ target }: React.ChangeEvent<HTMLInputElement>): void => {
      const matchingSuggestion = getFindingMatchingSuggestion(target.value);
      if (!_.isUndefined(matchingSuggestion)) {
        setAddFindingInitialValues({
          ...addFindingInitialValues,
          description: matchingSuggestion.description.includes("__empty__")
            ? ""
            : matchingSuggestion.description,
          recommendation: matchingSuggestion.recommendation.includes(
            "__empty__"
          )
            ? ""
            : matchingSuggestion.recommendation,
        });
      }
    },
    [addFindingInitialValues, getFindingMatchingSuggestion]
  );

  return (
    <React.StrictMode>
      {!loading && _.isEmpty(findings) && !_.isEmpty(activeRoots) ? (
        <Empty
          srcImage={searchingFindings}
          subtitle={t("searchFindings.noFindingsFound.subtitle")}
          title={t("searchFindings.noFindingsFound.title")}
        />
      ) : (
        <Table
          columnToggle={true}
          columnVisibilitySetter={setColumnVisibility}
          columnVisibilityState={columnVisibility}
          columns={tableColumns}
          data={filteredFindings}
          expandedRow={handleRowExpand}
          extraButtons={
            <React.Fragment>
              <Can I={"api_mutations_add_finding_mutate"}>
                <Tooltip
                  id={"group.findings.buttons.add.tooltip.id"}
                  tip={t("group.findings.buttons.add.tooltip")}
                >
                  <Button
                    icon={faPlus}
                    id={"addFinding"}
                    onClick={openAddFindingModal}
                  >
                    {t("group.findings.buttons.add.text")}
                  </Button>
                </Tooltip>
              </Can>
              <Can do={"api_mutations_remove_finding_mutate"}>
                <Tooltip
                  id={"group.findings.buttons.delete.tooltip"}
                  tip={t("group.findings.buttons.delete.tooltip")}
                >
                  <Button
                    disabled={selectedFindings.length === 0 || deleting}
                    icon={faTrashAlt}
                    onClick={openDeleteModal}
                  >
                    {t("group.findings.buttons.delete.text")}
                  </Button>
                </Tooltip>
              </Can>
              <Can I={"api_resolvers_query_report__get_url_group_report"}>
                <Tooltip
                  id={"group.findings.buttons.report.tooltip.id"}
                  tip={t("group.findings.buttons.report.tooltip")}
                >
                  <Button
                    icon={faArrowRight}
                    iconSide={"right"}
                    id={"reports"}
                    onClick={openReportsModal}
                    variant={"primary"}
                  >
                    {t("group.findings.buttons.report.text")}
                  </Button>
                </Tooltip>
              </Can>
            </React.Fragment>
          }
          filters={
            <Filters
              dataset={findings}
              filters={filters}
              permaset={[filterVal, setFilterVal]}
              setFilters={setFilters}
            />
          }
          id={"tblFindings"}
          onRowClick={goToFinding}
          onSearch={handleSearch}
          rowSelectionSetter={
            permissions.can("api_mutations_remove_finding_mutate")
              ? setSelectedFindings
              : undefined
          }
          rowSelectionState={selectedFindings}
          searchPlaceholder={t("searchFindings.searchPlaceholder")}
          sortingSetter={setSorting}
          sortingState={sorting}
        />
      )}

      <ReportsModal
        enableCerts={hasMachine && filledGroupInfo}
        isOpen={isReportsModalOpen}
        onClose={closeReportsModal}
        typesOptions={Object.keys(typesOptions)}
        userRole={data?.group.userRole ?? "user"}
      />
      <Modal
        onClose={closeAddFindingModal}
        open={isAddFindingModalOpen}
        title={t("group.findings.addModal.title")}
      >
        <Formik
          enableReinitialize={true}
          initialValues={addFindingInitialValues}
          name={"addFinding"}
          onSubmit={handleAdd}
        >
          {({ isValid }): JSX.Element => {
            return (
              <Form>
                <Label
                  htmlFor={"title"}
                  tooltip={t("searchFindings.tabDescription.title.tooltip")}
                >
                  {t("group.findings.addModal.title.label")}
                </Label>
                <Field
                  component={FormikAutocompleteText}
                  field={{ onChange: handleAddFindingTitleChange }}
                  focus={true}
                  id={"title"}
                  name={"title"}
                  suggestions={
                    _.isUndefined(suggestions)
                      ? []
                      : _.sortBy(
                          suggestions.map(
                            (suggestion: IFindingSuggestionData): string =>
                              `${suggestion.code}. ${suggestion.title}`
                          )
                        )
                  }
                  type={"text"}
                />
                <TextArea
                  label={t("group.findings.addModal.description.label")}
                  name={"description"}
                  tooltip={t("searchFindings.tabDescription.threat.tooltip")}
                />
                <TextArea
                  label={t("group.findings.addModal.recommendation.label")}
                  name={"recommendation"}
                  tooltip={t(
                    "searchFindings.tabDescription.recommendation.tooltip"
                  )}
                />
                <ModalConfirm
                  disabled={!isValid || addingFinding}
                  onCancel={closeAddFindingModal}
                />
              </Form>
            );
          }}
        </Formik>
      </Modal>
      <Modal
        onClose={closeDeleteModal}
        open={isDeleteModalOpen}
        title={t("group.findings.deleteModal.title")}
      >
        <Formik
          enableReinitialize={true}
          initialValues={{}}
          name={"removeVulnerability"}
          onSubmit={handleDelete}
        >
          <Form id={"removeVulnerability"}>
            <FormGroup>
              <ControlLabel>
                {t("group.findings.deleteModal.justification.label")}
              </ControlLabel>
              <Select
                name={"justification"}
                validate={composeValidators([required])}
              >
                <option value={""} />
                <option value={"DUPLICATED"}>
                  {t("group.findings.deleteModal.justification.duplicated")}
                </option>
                <option value={"FALSE_POSITIVE"}>
                  {t("group.findings.deleteModal.justification.falsePositive")}
                </option>
                <option value={"NOT_REQUIRED"}>
                  {t("group.findings.deleteModal.justification.notRequired")}
                </option>
              </Select>
            </FormGroup>
            <ModalConfirm disabled={isRunning} onCancel={closeDeleteModal} />
          </Form>
        </Formik>
      </Modal>
      <ExpertButton />
      {!loading && filteredFindings.length > 0 ? (
        <RiskExposureTour
          findingId={filteredFindings[0].id}
          findingRiskExposure={formatPercentage(
            getRiskExposure(
              filteredFindings[0].status,
              filteredFindings[0].severityScore,
              groupCVSSF
            ),
            true
          )}
          step={1}
        />
      ) : null}
      <WelcomeModal />
    </React.StrictMode>
  );
};

export { GroupFindingsView };
