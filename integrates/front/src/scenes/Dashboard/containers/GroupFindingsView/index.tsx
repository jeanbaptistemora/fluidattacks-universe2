/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint @typescript-eslint/no-unnecessary-condition:0 */
import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type {
  ColumnDef,
  ColumnFilter,
  ColumnFiltersState,
  Row,
  SortingState,
  VisibilityState,
} from "@tanstack/react-table";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useEffect, useMemo, useState } from "react";
import type { FormEvent } from "react";
import { useTranslation } from "react-i18next";
import { useHistory, useParams, useRouteMatch } from "react-router-dom";

import { renderDescription } from "./description";
import { locationsFormatter } from "./formatters/locationsFormatter";
import { GET_GROUP_VULNERABILITIES } from "./queries";
import type {
  IGroupVulnerabilities,
  IVulnerabilitiesResume,
  IVulnerability,
} from "./types";
import {
  formatFindings,
  formatState,
  getAreAllMutationValid,
  getResults,
  handleRemoveFindingsError,
} from "./utils";

import { REMOVE_FINDING_MUTATION } from "../FindingContent/queries";
import { formatPercentage } from "../GroupToeLinesView/utils";
import { Button } from "components/Button";
import { Modal, ModalConfirm } from "components/Modal";
import { Table } from "components/Table";
import { filterDate } from "components/Table/filters/filterFunctions/filterDate";
import type { ICellHelper } from "components/Table/types";
import { Tooltip } from "components/Tooltip";
import { GET_FINDINGS } from "scenes/Dashboard/containers/GroupFindingsView/queries";
import { ReportsModal } from "scenes/Dashboard/containers/GroupFindingsView/reportsModal";
import type {
  IFindingAttr,
  IGroupFindingsAttr,
} from "scenes/Dashboard/containers/GroupFindingsView/types";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { FormikDropdown } from "utils/forms/fields";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { composeValidators, required } from "utils/validations";

const GroupFindingsView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const { push } = useHistory();
  const { url } = useRouteMatch();
  const { t } = useTranslation();

  // State management
  const [isReportsModalOpen, setIsReportsModalOpen] = useState(false);
  const [vulnFilters, setVulnFilters] = useStoredState<ColumnFiltersState>(
    "vulnerabilitiesTable-columnFilters",
    [],
    localStorage
  );
  const [columnFilters, setColumnFilters] = useStoredState<ColumnFiltersState>(
    "tblFindings-columnFilters",
    [],
    localStorage
  );
  const [columnVisibility, setColumnVisibility] =
    useStoredState<VisibilityState>("tblFindings-visibilityState", {
      Asignees: false,
      Locations: false,
      Treatment: false,
      description: false,
      reattack: false,
      releaseDate: false,
    });
  const [sorting, setSorting] = useStoredState<SortingState>(
    "tblFindings-sortingState",
    []
  );
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

  function goToFinding(rowInfo: Row<IFindingAttr>): (event: FormEvent) => void {
    return (event: FormEvent): void => {
      push(`${url}/${rowInfo.original.id}/locations`);
      event.preventDefault();
    };
  }

  const handleQryErrors: (error: ApolloError) => void = useCallback(
    ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading group data", error);
      });
    },
    [t]
  );

  const tableColumns: ColumnDef<IFindingAttr>[] = [
    {
      accessorKey: "title",
      header: "Type",
      meta: { filterType: "select" },
    },
    {
      accessorKey: "age",
      header: "Age",
      meta: { filterType: "number" },
    },
    {
      accessorKey: "lastVulnerability",
      cell: (cell: ICellHelper<IFindingAttr>): string =>
        t("group.findings.description.value", { count: cell.getValue() }),
      header: "Last report",
      meta: { filterType: "number" },
    },
    {
      accessorKey: "state",
      cell: (cell: ICellHelper<IFindingAttr>): JSX.Element =>
        formatState(cell.getValue()),
      header: "Status",
      meta: { filterType: "select" },
    },
    {
      accessorKey: "severityScore",
      header: "Severity",
      meta: { filterType: "numberRange" },
    },
    {
      accessorKey: "openVulnerabilities",
      header: "Open Vulnerabilities",
    },
    {
      accessorKey: "closingPercentage",
      cell: (cell: ICellHelper<IFindingAttr>): string =>
        formatPercentage(cell.getValue()),
      header: t("group.findings.closingPercentage"),
      meta: { filterType: "number" },
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
      meta: { filterType: "select" },
    },
    {
      accessorFn: (row: IFindingAttr): string[] =>
        Array.from(row.locationsInfo.treatmentAssignmentEmails.values()),
      filterFn: "arrIncludes",
      header: "Asignees",
      meta: { filterType: "select" },
    },
    {
      accessorKey: "releaseDate",
      filterFn: filterDate,
      header: "Release Date",
      meta: { filterType: "dateRange" },
    },
    {
      accessorFn: (row: IFindingAttr): string[] => {
        const treatment = row.treatmentSummary;
        const treatmentNew = treatment.new > 0 ? "New" : "";
        const treatmentAccUndef =
          treatment.acceptedUndefined > 0 ? "Permanently Accepted" : "";
        const treatmentInProgress =
          treatment.inProgress > 0 ? "in Progress" : "";
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

        return `New: ${treatment.new}, in Progress: ${treatment.inProgress},
        Temporarily Accepted:  ${treatment.accepted}, Permamently Accepted:
        ${treatment.acceptedUndefined}`;
      },
      filterFn: "arrIncludes",
      header: "Treatment",
      meta: { filterType: "select" },
    },
    {
      accessorKey: "description",
      header: "Description",
    },
  ];

  const { data, refetch } = useQuery<IGroupFindingsAttr>(GET_FINDINGS, {
    fetchPolicy: "cache-first",
    onError: handleQryErrors,
    variables: { groupName },
  });

  const { data: vulnData, fetchMore } = useQuery<IGroupVulnerabilities>(
    GET_GROUP_VULNERABILITIES,
    {
      fetchPolicy: "cache-and-network",
      nextFetchPolicy: "cache-first",
      variables: { first: 1200, groupName },
    }
  );

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
                  vulnerability.currentState === "open"
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

      if (vulnData.group.vulnerabilities.pageInfo.hasNextPage) {
        void fetchMore({
          variables: {
            after: vulnData.group.vulnerabilities.pageInfo.endCursor,
          },
        });
      }
    }
  }, [vulnData, fetchMore]);

  const hasMachine = data?.group.hasMachine ?? false;
  const filledGroupInfo =
    !_.isEmpty(data?.group.description) &&
    !_.isEmpty(data?.group.businessId) &&
    !_.isEmpty(data?.group.businessName);

  const findings: IFindingAttr[] = useMemo(
    (): IFindingAttr[] =>
      data === undefined
        ? []
        : formatFindings(data.group.findings, findingVulnerabilities),
    [data, findingVulnerabilities]
  );

  const typesArray = findings.map((find: IFindingAttr): string[] => [
    find.title,
    find.title,
  ]);
  const typesOptions = Object.fromEntries(
    _.sortBy(typesArray, (arr): string => arr[0])
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

  const validMutationsHelper = (
    handleCloseModal: () => void,
    areAllMutationValid: boolean[]
  ): void => {
    if (areAllMutationValid.every(Boolean)) {
      msgSuccess(
        t("searchFindings.findingsDeleted"),
        t("group.drafts.titleSuccess")
      );
      void refetch();
      handleCloseModal();
    }
  };

  const handleRemoveFinding = async (justification: unknown): Promise<void> => {
    if (selectedFindings.length === 0) {
      msgError(t("searchFindings.tabResources.noSelection"));
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
  };

  function handleDelete(values: Record<string, unknown>): void {
    void handleRemoveFinding(values.justification);
  }

  function handleRowExpand(row: Row<IFindingAttr>): JSX.Element {
    return renderDescription(row.original);
  }

  useEffect((): void => {
    if (
      columnFilters.filter(
        (element: ColumnFilter): boolean => element.id === "state"
      ).length > 0
    ) {
      const filtervalue = columnFilters.filter(
        (element: ColumnFilter): boolean => element.id === "state"
      )[0].value;
      if (
        vulnFilters.filter(
          (element: ColumnFilter): boolean => element.id === "currentState"
        ).length > 0
      ) {
        setVulnFilters(
          vulnFilters.map((element: ColumnFilter): ColumnFilter => {
            if (element.id === "currentState") {
              return { id: "currentState", value: filtervalue };
            }

            return element;
          })
        );
      } else {
        setVulnFilters([
          ...vulnFilters,
          { id: "currentState", value: filtervalue },
        ]);
      }
    } else {
      setVulnFilters(
        vulnFilters
          .map((element: ColumnFilter): ColumnFilter => {
            if (element.id === "currentState") {
              return { id: "", value: "" };
            }

            return element;
          })
          .filter((element: ColumnFilter): boolean => element.id !== "")
      );
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [columnFilters]);

  return (
    <React.StrictMode>
      <Table
        columnFilterSetter={setColumnFilters}
        columnFilterState={columnFilters}
        columnToggle={true}
        columnVisibilitySetter={setColumnVisibility}
        columnVisibilityState={columnVisibility}
        columns={tableColumns}
        data={findings}
        enableColumnFilters={true}
        expandedRow={handleRowExpand}
        extraButtons={
          <React.Fragment>
            <Can I={"api_resolvers_query_report__get_url_group_report"}>
              <Tooltip
                id={"group.findings.report.btn.tooltip.id"}
                tip={t("group.findings.report.btn.tooltip")}
              >
                <Button
                  id={"reports"}
                  onClick={openReportsModal}
                  variant={"primary"}
                >
                  {t("group.findings.report.btn.text")}
                </Button>
              </Tooltip>
            </Can>
            <Can do={"api_mutations_remove_finding_mutate"}>
              <Tooltip
                id={"searchFindings.delete.btn.tooltip"}
                tip={t("searchFindings.delete.btn.tooltip")}
              >
                <Button
                  disabled={selectedFindings.length === 0 || deleting}
                  onClick={openDeleteModal}
                  variant={"secondary"}
                >
                  <FontAwesomeIcon icon={faTrashAlt} />
                  &nbsp;{t("searchFindings.delete.btn.text")}
                </Button>
              </Tooltip>
            </Can>
          </React.Fragment>
        }
        id={"tblFindings"}
        onRowClick={goToFinding}
        rowSelectionSetter={
          permissions.can("api_mutations_remove_finding_mutate")
            ? setSelectedFindings
            : undefined
        }
        rowSelectionState={selectedFindings}
        sortingSetter={setSorting}
        sortingState={sorting}
      />
      <ReportsModal
        enableCerts={hasMachine && filledGroupInfo}
        isOpen={isReportsModalOpen}
        onClose={closeReportsModal}
        typesOptions={Object.keys(typesOptions)}
        userRole={data?.group.userRole ?? "user"}
      />
      <Modal
        onClose={closeDeleteModal}
        open={isDeleteModalOpen}
        title={t("searchFindings.delete.title")}
      >
        <Formik
          enableReinitialize={true}
          initialValues={{}}
          name={"removeFinding"}
          onSubmit={handleDelete}
        >
          <Form id={"removeFinding"}>
            <FormGroup>
              <ControlLabel>
                {t("searchFindings.delete.justif.label")}
              </ControlLabel>
              <Field
                component={FormikDropdown}
                name={"justification"}
                validate={composeValidators([required])}
              >
                <option value={""} />
                <option value={"DUPLICATED"}>
                  {t("searchFindings.delete.justif.duplicated")}
                </option>
                <option value={"FALSE_POSITIVE"}>
                  {t("searchFindings.delete.justif.falsePositive")}
                </option>
                <option value={"NOT_REQUIRED"}>
                  {t("searchFindings.delete.justif.notRequired")}
                </option>
              </Field>
            </FormGroup>
            <ModalConfirm disabled={isRunning} onCancel={closeDeleteModal} />
          </Form>
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { GroupFindingsView };
