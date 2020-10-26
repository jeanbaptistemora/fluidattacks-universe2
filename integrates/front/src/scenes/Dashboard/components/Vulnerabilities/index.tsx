/* tslint:disable: jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that defines the headers of the table
*/
import { QueryResult } from "@apollo/react-common";
import { Query } from "@apollo/react-components";
import { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React, { useState } from "react";
import { Col, Row } from "react-bootstrap";
import { Comparator, textFilter } from "react-bootstrap-table2-filter";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import { deleteFormatter, statusFormatter } from "components/DataTableNext/formatters";
import { proFormatter } from "components/DataTableNext/headerFormatters/proFormatter";
import { IHeaderConfig } from "components/DataTableNext/types";
import { FluidIcon } from "components/FluidIcon";
import {
  deleteVulnerabilityModal as DeleteVulnerabilityModal,
} from "scenes/Dashboard/components/DeleteVulnerability/index";
import { IDeleteVulnAttr } from "scenes/Dashboard/components/DeleteVulnerability/types";
import { default as style } from "scenes/Dashboard/components/Vulnerabilities/index.css";
import { GET_VULNERABILITIES } from "scenes/Dashboard/components/Vulnerabilities/queries";
import {
  IVulnDataType, IVulnerabilitiesViewProps, IVulnRow, IVulnsAttr, IVulnType,
} from "scenes/Dashboard/components/Vulnerabilities/types";
import { UpdateTreatmentModal } from "scenes/Dashboard/components/Vulnerabilities/updateTreatment";
import { UploadVulnerabilites } from "scenes/Dashboard/components/Vulnerabilities/uploadFile";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const filterState:
  ((dataVuln: IVulnType, state: string) => IVulnType) =
    (dataVuln: IVulnType, state: string): IVulnType =>

      dataVuln.filter((vuln: IVulnType[0]) => !_.isUndefined(vuln.lastApprovedStatus) ?
      vuln.lastApprovedStatus === state : vuln.currentState === state);

const specificToNumber: ((line: IVulnRow) => number) =
  (line: IVulnRow): number =>
    parseInt(line.specific, 10);

const getSpecific: ((line: IVulnRow) => string) =
  (line: IVulnRow): string =>
    line.specific;

const getSeverity: ((line: IVulnRow) => string) =
  (line: IVulnRow): string =>
    !_.isEqual(line.severity, "-1") ? line.severity : "";

const getTag: ((line: IVulnRow) => string) =
  (line: IVulnRow): string =>
    line.tag;

const getTreatmentManager: ((line: IVulnRow) => string) =
  (line: IVulnRow): string =>
    line.treatmentManager;

export const compareNumbers: ((a: number, b: number) => number) =
  (a: number, b: number): number =>
    a - b;

const negativeInParens: ((num: number) => string) =
  (num: number): string  =>
  num < 0 ? `(${num})` : num.toString();

const getRanges: ((array: number[]) => string) =
 (array: number[]): string => {
  const ranges: string[] = [];
  let index: number;
  for (index = 0; index < array.length; index++) {
    const rstart: number = array[index];
    let rend: number = rstart;
    while (array[index + 1] - array[index] === 1) {
      rend = array[index + 1];
      index++;
    }
    ranges.push(
      rstart === rend ? `${negativeInParens(rstart)}` : `${negativeInParens(rstart)}-${negativeInParens(rend)}`);
  }

  return ranges.join(", ");
};

const groupValues: ((values: number[]) => string) = (values: number[]): string => {
  values.sort(compareNumbers);

  return getRanges(values);
};

const groupVerification: ((lines: IVulnRow[]) => string) = (lines: IVulnRow[]): string =>
  lines.every((row: IVulnRow) => row.verification === "Requested") ? "Requested" :
    lines.every((row: IVulnRow) => row.verification === "Verified (open)") ? "Verified (open)" : "";

const groupSpecific: ((lines: IVulnType) => IVulnType) = (lines: IVulnType): IVulnType => {
  const groups: { [key: string]: IVulnType }  = _.groupBy(lines, "where");
  const specificGrouped: IVulnType = _.map(groups, (line: IVulnType) =>
    ({
        acceptanceDate: "",
        analyst: "",
        currentApprovalStatus: line[0].currentApprovalStatus,
        currentState: line[0].currentState,
        id: line[0].id,
        isNew: line[0].isNew,
        lastAnalyst: "",
        lastApprovedStatus: line[0].lastApprovedStatus,
        remediated: line.every((row: IVulnRow) => row.remediated),
        severity: line.map(getSeverity)
          .filter(Boolean)
          .join(", "),
        specific: line[0].vulnType === "inputs" ? line.map(getSpecific)
          .join(", ") : groupValues(line.map(specificToNumber)),
        tag: Array.from(new Set(line.map(getTag)))
          .filter(Boolean)
          .join(", "),
        treatmentManager: Array.from(new Set(line.map(getTreatmentManager)))
          .filter(Boolean)
          .join(", "),
        verification: groupVerification(line),
        vulnType: line[0].vulnType,
        where: line[0].where,
    }));

  return specificGrouped;
};

const newVulnerabilities: ((lines: IVulnType) => IVulnType) = (lines: IVulnType): IVulnType => (
    _.map(lines, (line: IVulnType[0]) =>
      ({
        analyst: line.analyst,
        currentApprovalStatus: line.currentApprovalStatus,
        currentState: line.currentState,
        id: line.id,
        isNew: _.isEmpty(line.lastApprovedStatus) ?
        translate.t("search_findings.tab_description.new") :
        translate.t("search_findings.tab_description.old"),
        lastAnalyst: line.lastAnalyst,
        lastApprovedStatus: line.lastApprovedStatus,
        remediated: line.remediated,
        severity: getSeverity(line),
        specific: line.specific,
        tag: line.tag,
        treatmentManager: line.treatmentManager,
        verification: line.verification === "Verified"
          ? `${line.verification} (${line.currentState})`
          : line.verification,
        vulnType: line.vulnType,
        where: line.where,
      })));

const getVulnByRow: (selectedRowId: string, categoryVuln: IVulnRow[], vulnData: IVulnDataType[]) =>
  IVulnDataType[] = (selectedRowId: string, categoryVuln: IVulnRow[], vulnData: IVulnDataType[]):
  IVulnDataType[] => {
    categoryVuln.forEach((vuln: {
      currentState: string;
      id: string;
      severity: string;
      specific: string;
      tag: string;
      treatmentManager: string;
      where: string;
    }) => {
      if (selectedRowId === vuln.id) {
      vulnData.push({
        currentState: vuln.currentState,
        id: vuln.id,
        specific: vuln.specific,
        treatments: {
          severity: vuln.severity,
          tag: vuln.tag,
          treatmentManager: vuln.treatmentManager,
        },
        where: vuln.where,
      });
    }
  });

    return vulnData;
  };

const getVulnInfo: (selectedRowArray: string[], arrayVulnCategory: IVulnRow[][]) =>
  IVulnDataType[] = (selectedRowArray: string[], arrayVulnCategory: IVulnRow[][]):
  IVulnDataType[] => {
  let arrayVulnInfo: IVulnDataType[] = [];
  selectedRowArray.forEach((selectedRow: string) => {
    if (!_.isUndefined(selectedRow)) {
      arrayVulnCategory.forEach((category: IVulnRow[]) => {
        arrayVulnInfo = getVulnByRow(selectedRow, category, arrayVulnInfo);
      });
    }
  });

  return arrayVulnInfo;
  };

interface ICalculateRowsSelected {
  oneRowSelected: boolean;
  vulns: IVulnDataType[];
}

const vulnsViewComponent: React.FC<IVulnerabilitiesViewProps> =
  (props: IVulnerabilitiesViewProps): JSX.Element => {
    const permissions: PureAbility<string> = useAbility(authzPermissionsContext);

    // State management
    const [modalHidden, setModalHidden] = useState(false);
    const [deleteVulnModal, setDeleteVulnModal] = useState(false);
    const [vulnerabilityId, setVulnerabilityId] = useState("");
    const emptyArray: string[] = [];
    const [arraySelectedRows, setArraySelectedRows] = useState(emptyArray);
    const [selectRowsInputs, setSelectRowsInputs] = useState<number[]>([]);
    const [selectRowsLines, setSelectRowsLines] = useState<number[]>([]);
    const [selectRowsPorts, setSelectRowsPorts] = useState<number[]>([]);

    const isEditing: boolean = props.editMode
      || props.isRequestVerification === true
      || props.isVerifyRequest === true;

    const canGetAnalyst: boolean = permissions.can("backend_api_resolvers_new_finding_analyst_resolve");
    const shouldGroup: boolean = !isEditing && props.separatedRow === true;

    const handleOpenVulnSetClick: () => void = (): void => {
      setModalHidden(true);
    };

    const handleCloseTableSetClick: () => void = (): void => {
      setModalHidden(false);
    };

    const handleCloseDeleteVulnModal: (() => void) = (): void => {
      setDeleteVulnModal(false);
    };

    const handleDeleteVulnerability: ((vulnInfo: { [key: string]: string } | undefined) => void) =
    (vulnInfo: { [key: string]: string } | undefined): void => {
      if (vulnInfo !== undefined) {
        setVulnerabilityId(vulnInfo.id);
        setDeleteVulnModal(true);
      }
    };

    const clearSelectedRows: (() => void) = (): void => {
      setSelectRowsInputs([]);
      setSelectRowsLines([]);
      setSelectRowsPorts([]);
      setArraySelectedRows([]);
    };

    const handleQueryError: ((error: ApolloError) => void) = (
      { graphQLErrors }: ApolloError,
    ): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred getting vulnerabilities", error);
      });
    };

    return(
    <Query
      query={GET_VULNERABILITIES}
      variables={{ analystField: canGetAnalyst, identifier: props.findingId }}
      onError={handleQueryError}
    >
      {({ data, refetch }: QueryResult<IVulnsAttr>): JSX.Element => { // tslint:disable-next-line: cyclomatic-complexity
          if (_.isUndefined(data) || _.isEmpty(data)) {

            return <React.Fragment/>;
          }

          if (!_.isUndefined(data)) {

            const dataInputs: IVulnsAttr["finding"]["inputsVulns"] = newVulnerabilities(filterState(
              data.finding.inputsVulns, props.state));
            const dataLines: IVulnsAttr["finding"]["linesVulns"] = newVulnerabilities(filterState(
              data.finding.linesVulns, props.state));
            const dataPorts: IVulnsAttr["finding"]["portsVulns"] = newVulnerabilities(filterState(
              data.finding.portsVulns, props.state));

            const handleMtDeleteVulnRes: ((mtResult: IDeleteVulnAttr) => void) = (mtResult: IDeleteVulnAttr): void => {
              if (!_.isUndefined(mtResult)) {
                if (mtResult.deleteVulnerability.success) {
                  setDeleteVulnModal(false);
                  void refetch();
                  mixpanel.track(
                    "DeleteVulnerability",
                    {
                      User: (window as typeof window & { userName: string }).userName,
                    });
                  msgSuccess(
                    translate.t("search_findings.tab_description.vulnDeleted"),
                    translate.t("group_alerts.title_success"));
                } else {
                  msgError(
                    translate.t("delete_vulns.not_success"),
                  );
                  setDeleteVulnModal(false);
                }
              }
            };

            const onSortInputs: ((dataField: string, order: SortOrder) => void) = (
              dataField: string, order: SortOrder,
            ): void => {
              const newSorted: Sorted = { dataField, order };
              sessionStorage.setItem("vulnInputsSort", JSON.stringify(newSorted));
            };
            const onFilterInputs: ((filterVal: string) => void) = (filterVal: string): void => {
              sessionStorage.setItem("vulnInputsFilter", filterVal);
            };
            const onSortLines: ((dataField: string, order: SortOrder) => void) = (
              dataField: string, order: SortOrder,
            ): void => {
              const newSorted: Sorted = { dataField, order };
              sessionStorage.setItem("vulnLinesSort", JSON.stringify(newSorted));
            };
            const onFilterLines: ((filterVal: string) => void) = (filterVal: string): void => {
              sessionStorage.setItem("vulnLinesFilter", filterVal);
            };
            const onSortPorts: ((dataField: string, order: SortOrder) => void) = (
              dataField: string, order: SortOrder,
            ): void => {
              const newSorted: Sorted = { dataField, order };
              sessionStorage.setItem("vulnPortsSort", JSON.stringify(newSorted));
            };
            const onFilterPorts: ((filterVal: string) => void) = (filterVal: string): void => {
              sessionStorage.setItem("vulnPortsFilter", filterVal);
            };
            const columnFilter: TextFilterProps = {
              className: style.filter_input,
              comparator: Comparator.LIKE,
              delay: 1000,
            };
            const inputsHeader: IHeaderConfig[] = [
            {
              align: "left",
              dataField: "where",
              filter: textFilter({
                ...columnFilter,
                defaultValue: _.get(sessionStorage, "vulnInputsFilter"),
                onFilter: onFilterInputs,
              }),
              header: "URL",
              onSort: onSortInputs,
            },
            {
              align: "left",
              dataField: "specific",
              header: translate.t("search_findings.tab_description.field"),
              onSort: onSortInputs,
            }];
            const linesHeader: IHeaderConfig[] = [
              {
                align: "left",
                dataField: "where",
                filter: textFilter({
                  ...columnFilter,
                  defaultValue: _.get(sessionStorage, "vulnLinesFilter"),
                  onFilter: onFilterLines,
                }),
                header: translate.t("search_findings.tab_description.path"),
                onSort: onSortLines,
              },
              {
                align: "left",
                dataField: "specific",
                header: translate.t("search_findings.tab_description.line", {count: 1}),
                onSort: onSortLines,
                wrapped: true,
              }];
            const portsHeader: IHeaderConfig[] = [
              {
                align: "left",
                dataField: "where",
                filter: textFilter({
                  ...columnFilter,
                  defaultValue: _.get(sessionStorage, "vulnPortsFilter"),
                  onFilter: onFilterPorts,
                }),
                header: "Host",
                onSort: onSortPorts,
              },
              {
                align: "left",
                dataField: "specific",
                header: translate.t("search_findings.tab_description.port", {count: 1}),
                onSort: onSortPorts,
                wrapped: true,
              }];

            let formattedDataLines: IVulnsAttr["finding"]["linesVulns"] = dataLines;
            let formattedDataPorts: IVulnsAttr["finding"]["portsVulns"] = dataPorts;
            let formattedDataInputs: IVulnsAttr["finding"]["inputsVulns"] = dataInputs;

            inputsHeader.push(
              {
                align: "left",
                dataField: "verification",
                formatter: statusFormatter,
                header: translate.t("search_findings.tab_description.verification"),
                onSort: onSortInputs,
              },
              {
                align: "left",
                dataField: "tag",
                header: translate.t("search_findings.tab_description.tag"),
                headerFormatter: proFormatter,
                onSort: onSortInputs,
              },
              {
                align: "left",
                dataField: "severity",
                header: translate.t("search_findings.tab_description.business_criticality"),
                headerFormatter: proFormatter,
                onSort: onSortInputs,
              },
              {
                align: "left",
                dataField: "treatmentManager",
                header: translate.t("search_findings.tab_description.treatment_mgr"),
                onSort: onSortInputs,
                width: "30%",
              },
            );
            linesHeader.push(
              {
                align: "left",
                dataField: "verification",
                formatter: statusFormatter,
                header: translate.t("search_findings.tab_description.verification"),
                onSort: onSortLines,
              },
              {
                align: "left",
                dataField: "tag",
                header: translate.t("search_findings.tab_description.tag"),
                headerFormatter: proFormatter,
                onSort: onSortLines,
              },
              {
                align: "left",
                dataField: "severity",
                header: translate.t("search_findings.tab_description.business_criticality"),
                headerFormatter: proFormatter,
                onSort: onSortLines,
              },
              {
                align: "left",
                dataField: "treatmentManager",
                header: translate.t("search_findings.tab_description.treatment_mgr"),
                onSort: onSortLines,
              },
            );
            portsHeader.push(
              {
                align: "left",
                dataField: "verification",
                formatter: statusFormatter,
                header: translate.t("search_findings.tab_description.verification"),
                onSort: onSortPorts,
              },
              {
                align: "left",
                dataField: "tag",
                header: translate.t("search_findings.tab_description.tag"),
                headerFormatter: proFormatter,
                onSort: onSortPorts,
                wrapped: true,
              },
              {
                align: "left",
                dataField: "severity",
                header: translate.t("search_findings.tab_description.business_criticality"),
                headerFormatter: proFormatter,
                onSort: onSortPorts,
              },
              {
                align: "left",
                dataField: "treatmentManager",
                header: translate.t("search_findings.tab_description.treatment_mgr"),
                onSort: onSortPorts,
              },
            );

            if (props.editMode && permissions.can("backend_api_resolvers_vulnerability__do_delete_vulnerability")) {
              inputsHeader.push({
                          align: "center",
                          dataField: "id",
                          deleteFunction: handleDeleteVulnerability,
                          formatter: deleteFormatter,
                          header: translate.t("search_findings.tab_description.action"),
                        });
              linesHeader.push({
                          align: "center",
                          dataField: "id",
                          deleteFunction: handleDeleteVulnerability,
                          formatter: deleteFormatter,
                          header: translate.t("search_findings.tab_description.action"),
                        });
              portsHeader.push({
                          align: "center",
                          dataField: "id",
                          deleteFunction: handleDeleteVulnerability,
                          formatter: deleteFormatter,
                          header: translate.t("search_findings.tab_description.action"),
                          width: "10%",
                        });
            } else if (canGetAnalyst) {
              inputsHeader.push({
                align: "left",
                dataField: "lastAnalyst",
                header: translate.t("search_findings.tab_description.analyst"),
              });
              linesHeader.push({
                align: "left",
                dataField: "lastAnalyst",
                header: translate.t("search_findings.tab_description.analyst"),
              });
              portsHeader.push({
                align: "left",
                dataField: "lastAnalyst",
                header: translate.t("search_findings.tab_description.analyst"),
              });
            } else if (shouldGroup) {
              formattedDataLines = groupSpecific(dataLines);
              formattedDataPorts = groupSpecific(dataPorts);
              formattedDataInputs = groupSpecific(dataInputs);
            }

            const renderButtonUpdateVuln: (() => JSX.Element) =
            (): JSX.Element => (
                  <React.Fragment>
                    <Row>
                      <Col mdOffset={5} md={4}>
                        <Button
                          onClick={handleOpenVulnSetClick}
                          disabled={!(arraySelectedRows.length > 0)}
                        >
                          <FluidIcon icon="edit" /> {translate.t("search_findings.tab_description.editVuln")}
                        </Button>
                      </Col>
                    </Row><br/>
                </React.Fragment>
            );

            const calculateRowsSelected: () => ICalculateRowsSelected = (): ICalculateRowsSelected  => {
              const arrayVulnCategory: IVulnRow[][] = [
                data.finding.inputsVulns,
                data.finding.linesVulns,
                data.finding.portsVulns,
              ];
              const vulns: IVulnDataType[] = getVulnInfo(arraySelectedRows, arrayVulnCategory);

              return {
                oneRowSelected: vulns.length === 1,
                vulns,
              };
            };

            const renderRequestVerification: (() => JSX.Element) = (): JSX.Element => {
              const handleClick: (() => void) = (): void => {
                const selectedRows: ICalculateRowsSelected = calculateRowsSelected();
                const vulnerabilities: IVulnDataType[] = selectedRows.vulns;
                if (props.verificationFn !== undefined) {
                  props.verificationFn(vulnerabilities, "request", clearSelectedRows);
                }
              };

              return (
                <React.Fragment>
                  <Can do="backend_api_resolvers_vulnerability__do_request_verification_vuln">
                    <Row>
                      <Col mdOffset={5} md={4}>
                        <Button
                          id="request_verification_vulns"
                          onClick={handleClick}
                          disabled={!(arraySelectedRows.length > 0)}
                          type={"button"}
                        >
                          <FluidIcon icon="verified" /> {translate.t("search_findings.tab_description.request_verify.text")}
                        </Button>
                      </Col><br/>
                    </Row>
                  </Can>
                </React.Fragment>
              );
            };
            const renderVerifyRequest: (() => JSX.Element) = (): JSX.Element => {
              const handleClick: (() => void) = (): void => {
                const selectedRows: ICalculateRowsSelected = calculateRowsSelected();
                const vulnerabilities: IVulnDataType[] = selectedRows.vulns;
                if (props.verificationFn !== undefined) {
                  props.verificationFn(vulnerabilities, "verify", clearSelectedRows);
                }
              };

              return (
                <React.Fragment>
                  {props.isVerifyRequest === true ?
                    <Row>
                      <Col mdOffset={5} md={4}>
                        <Button
                          onClick={handleClick}
                          disabled={!(arraySelectedRows.length > 0)}
                        >
                          <FluidIcon icon="verified" /> {translate.t("search_findings.tab_description.mark_verified.text")}
                        </Button>
                      </Col><br/>
                    </Row>
                  : undefined}
                </React.Fragment>
              );
            };

            const rowsSelected: ICalculateRowsSelected = calculateRowsSelected();
            const vulnerabilitiesList: IVulnDataType[] = rowsSelected.vulns;

            const inputVulnsRemediated: number[] = dataInputs.reduce(
              (acc: number[], vuln: IVulnRow, index: number) => (vuln.remediated ? [...acc, index] : acc), []);
            const lineVulnsRemediated: number[] = dataLines.reduce(
              (acc: number[], vuln: IVulnRow, index: number) => (vuln.remediated ? [...acc, index] : acc), []);
            const portVulnsRemediated: number[] = dataPorts.reduce(
              (acc: number[], vuln: IVulnRow, index: number) => (vuln.remediated ? [...acc, index] : acc), []);
            const inputVulnsVerified: number[] = dataInputs.reduce(
              (acc: number[], vuln: IVulnRow, index: number) => (!vuln.remediated ? [...acc, index] : acc), []);
            const lineVulnsVerified: number[] = dataLines.reduce(
              (acc: number[], vuln: IVulnRow, index: number) => (!vuln.remediated ? [...acc, index] : acc), []);
            const portVulnsVerified: number[] = dataPorts.reduce(
              (acc: number[], vuln: IVulnRow, index: number) => (!vuln.remediated ? [...acc, index] : acc), []);
            const calculateNewIndex: ((rows: IVulnRow[], vulns: IVulnRow[]) => number[]) =
              (rows: IVulnRow[], vulns: IVulnRow[]): number[] => (vulns.reduce(
                (acc: number[], vuln: IVulnRow, indexReduce: number) =>
                  _.includes(rows.map((row: IVulnRow) => row.id), vuln.id) ? [...acc, indexReduce] : acc,
                []));

            const calculateIndex: ((row: IVulnRow, vulns: IVulnRow[]) => number) =
              (row: IVulnRow, vulns: IVulnRow[]): number => (
                vulns.reduce(
                  (acc: number, vuln: IVulnRow, indexR: number) => (vuln.id === row.id ? indexR : acc), 0));
            const handleOnSelectInputs: ((row: IVulnRow, isSelect: boolean) => void) =
            (row: IVulnRow, isSelect: boolean): void => {
              const index: number = calculateIndex(row, dataInputs);
              if (isSelect) {
                const newSet: Set<string> = new Set([...arraySelectedRows, row.id]);
                setArraySelectedRows(Array.from(newSet));
                setSelectRowsInputs([...selectRowsInputs, index]);
              } else {
                const newSet: Set<string> = new Set(arraySelectedRows.filter((rowId: string) => rowId !== row.id));
                setArraySelectedRows(Array.from(newSet));
                setSelectRowsInputs([...selectRowsInputs.filter((indexFilter: number) => indexFilter !== index)]);
              }
            };
            const handleOnSelectAllInputs: ((isSelect: boolean, rows: IVulnRow[]) => void) =
            (isSelect: boolean, rows: IVulnRow[]): void => {
              const newIds: string[] = rows.map((row: IVulnRow) => row.id);
              if (isSelect) {
                const newSet: Set<string> = new Set([...arraySelectedRows, ...newIds]);
                setArraySelectedRows(Array.from(newSet));
                let newArray: number[] = calculateNewIndex(rows, dataInputs);
                if (props.isRequestVerification === true) {
                  newArray = newArray.filter((indexFilter: number) =>
                    !_.includes(inputVulnsRemediated, indexFilter));
                } else if (props.isVerifyRequest === true) {
                  newArray = newArray.filter((indexFilter: number) =>
                    !_.includes(inputVulnsVerified, indexFilter));
                }
                const newSetInputs: Set<number> = new Set([...selectRowsInputs, ...newArray]);
                setSelectRowsInputs(Array.from(newSetInputs));
              } else {
                const newSet: Set<string> = new Set(arraySelectedRows);
                newIds.forEach((deleteRowId: string) => newSet.delete(deleteRowId));
                setArraySelectedRows(Array.from(newSet));
                setSelectRowsInputs([]);
              }
            };
            const handleOnSelectLines: ((row: IVulnRow, isSelect: boolean) => void) =
            (row: IVulnRow, isSelect: boolean): void => {
              const index: number = calculateIndex(row, dataLines);
              if (isSelect) {
                const newSet: Set<string> = new Set([...arraySelectedRows, row.id]);
                setArraySelectedRows(Array.from(newSet));
                setSelectRowsLines([...selectRowsLines, index]);
              } else {
                const newSet: Set<string> = new Set(arraySelectedRows.filter((rowId: string) => rowId !== row.id));
                setArraySelectedRows(Array.from(newSet));
                setSelectRowsLines([...selectRowsLines.filter((indexFilter: number) => indexFilter !== index)]);
              }
            };
            const handleOnSelectAllLines: ((isSelect: boolean, rows: IVulnRow[]) => void) =
            (isSelect: boolean, rows: IVulnRow[]): void => {
              const newIds: string[] = rows.map((row: IVulnRow) => row.id);
              if (isSelect) {
                const newSet: Set<string> = new Set([...arraySelectedRows, ...newIds]);
                setArraySelectedRows(Array.from(newSet));
                let newArray: number[] = calculateNewIndex(rows, dataLines);
                if (props.isRequestVerification === true) {
                  newArray = newArray.filter((indexFilter: number) =>
                    !_.includes(lineVulnsRemediated, indexFilter));
                } else if (props.isVerifyRequest === true) {
                  newArray = newArray.filter((indexFilter: number) =>
                    !_.includes(lineVulnsVerified, indexFilter));
                }
                const newSetLines: Set<number> = new Set([...selectRowsLines, ...newArray]);
                setSelectRowsLines(Array.from(newSetLines));
              } else {
                const newSet: Set<string> = new Set(arraySelectedRows);
                newIds.forEach((deleteRowId: string) => newSet.delete(deleteRowId));
                setArraySelectedRows(Array.from(newSet));
                setSelectRowsLines([]);
              }
            };
            const handleOnSelectPorts: ((row: IVulnRow, isSelect: boolean) => void) =
            (row: IVulnRow, isSelect: boolean): void => {
              const index: number = calculateIndex(row, dataPorts);
              if (isSelect) {
                const newSet: Set<string> = new Set([...arraySelectedRows, row.id]);
                setArraySelectedRows(Array.from(newSet));
                setSelectRowsPorts([...selectRowsPorts, index]);
              } else {
                const newSet: Set<string> = new Set(arraySelectedRows.filter((rowId: string) => rowId !== row.id));
                setArraySelectedRows(Array.from(newSet));
                setSelectRowsPorts([...selectRowsPorts.filter((indexFilter: number) => indexFilter !== index)]);
              }
            };
            const handleOnSelectAllPorts: ((isSelect: boolean, rows: IVulnRow[]) => void) =
            (isSelect: boolean, rows: IVulnRow[]): void => {
              const newIds: string[] = rows.map((row: IVulnRow) => row.id);
              if (isSelect) {
                const newSet: Set<string> = new Set([...arraySelectedRows, ...newIds]);
                setArraySelectedRows(Array.from(newSet));
                let newArray: number[] = calculateNewIndex(rows, dataPorts);
                if (props.isRequestVerification === true) {
                  newArray = newArray.filter((indexFilter: number) =>
                    !_.includes(portVulnsRemediated, indexFilter));
                } else if (props.isVerifyRequest === true) {
                  newArray = newArray.filter((indexFilter: number) =>
                    !_.includes(portVulnsVerified, indexFilter));
                }
                const newSetPorts: Set<number> = new Set([...selectRowsPorts, ...newArray]);
                setSelectRowsPorts(Array.from(newSetPorts));
              } else {
                const newSet: Set<string> = new Set(arraySelectedRows);
                newIds.forEach((deleteRowId: string) => newSet.delete(deleteRowId));
                setArraySelectedRows(Array.from(newSet));
                setSelectRowsPorts([]);
              }
            };
            const selectionModeInputs: SelectRowOptions = {
              clickToSelect: false,
              hideSelectColumn: !isEditing,
              mode: "checkbox",
              nonSelectable: props.isRequestVerification === true ? inputVulnsRemediated :
              props.isVerifyRequest === true ? inputVulnsVerified : undefined,
              onSelect: handleOnSelectInputs,
              onSelectAll: handleOnSelectAllInputs,
              selected: selectRowsInputs,
            };
            const selectionModeLines: SelectRowOptions = {
              clickToSelect: false,
              hideSelectColumn: !isEditing,
              mode: "checkbox",
              nonSelectable: props.isRequestVerification === true ? lineVulnsRemediated :
              props.isVerifyRequest === true ? lineVulnsVerified : undefined,
              onSelect: handleOnSelectLines,
              onSelectAll: handleOnSelectAllLines,
              selected: selectRowsLines,
            };
            const selectionModePorts: SelectRowOptions = {
              clickToSelect: false,
              hideSelectColumn: !isEditing,
              mode: "checkbox",
              nonSelectable: props.isRequestVerification === true ? portVulnsRemediated :
              props.isVerifyRequest === true ? portVulnsVerified : undefined,
              onSelect: handleOnSelectPorts,
              onSelectAll: handleOnSelectAllPorts,
              selected: selectRowsPorts,
            };

            return (
              <React.StrictMode>
                { dataInputs.length > 0
                  ? <React.Fragment>
                      <label className={style.vuln_title}>
                        {translate.t("search_findings.tab_description.inputs")}
                      </label>
                      <DataTableNext
                        id="inputsVulns"
                        bordered={false}
                        dataset={formattedDataInputs}
                        defaultSorted={JSON.parse(_.get(sessionStorage, "vulnInputsSort", "{}"))}
                        exportCsv={false}
                        headers={inputsHeader}
                        pageSize={10}
                        search={false}
                        selectionMode={selectionModeInputs}
                        tableBody={style.tableBody}
                        tableHeader={style.tableHeader}
                      />
                    </React.Fragment>
                  : undefined
                }
                { dataLines.length > 0
                  ? <React.Fragment>
                      <label className={style.vuln_title}>
                        {translate.t("search_findings.tab_description.line", {count: 2})}
                      </label>
                      <DataTableNext
                        id="linesVulns"
                        bordered={false}
                        dataset={formattedDataLines}
                        defaultSorted={JSON.parse(_.get(sessionStorage, "vulnLinesSort", "{}"))}
                        exportCsv={false}
                        headers={linesHeader}
                        pageSize={10}
                        search={false}
                        selectionMode={selectionModeLines}
                        tableBody={style.tableBody}
                        tableHeader={style.tableHeader}
                      />
                    </React.Fragment>
                  : undefined
                }
                { dataPorts.length > 0
                  ? <React.Fragment>
                      <label className={style.vuln_title}>
                        {translate.t("search_findings.tab_description.port", {count: 2})}
                      </label>
                      <DataTableNext
                        id="portsVulns"
                        bordered={false}
                        dataset={formattedDataPorts}
                        defaultSorted={JSON.parse(_.get(sessionStorage, "vulnPortsSort", "{}"))}
                        exportCsv={false}
                        headers={portsHeader}
                        pageSize={10}
                        search={false}
                        selectionMode={selectionModePorts}
                        tableBody={style.tableBody}
                        tableHeader={style.tableHeader}
                      />
                    </React.Fragment>
                  : undefined
                }
                <DeleteVulnerabilityModal
                  findingId={props.findingId}
                  id={vulnerabilityId}
                  open={deleteVulnModal}
                  onClose={handleCloseDeleteVulnModal}
                  onDeleteVulnRes={handleMtDeleteVulnRes}
                />
                { modalHidden ?
                  <UpdateTreatmentModal
                    btsUrl={props.btsUrl}
                    findingId={props.findingId}
                    lastTreatment={props.lastTreatment}
                    projectName={props.projectName}
                    vulnerabilities={vulnerabilitiesList}
                    handleCloseModal={handleCloseTableSetClick}
                  />
                : undefined }
                {props.editMode ? (
                  <React.Fragment>
                    <Can do="backend_api_resolvers_vulnerability__do_update_treatment_vuln">
                      {renderButtonUpdateVuln()}
                    </Can>
                    <Can do="backend_api_resolvers_vulnerability__do_upload_file">
                      <UploadVulnerabilites {...props} />
                    </Can>
                  </React.Fragment>
                ) : undefined}
                {props.isRequestVerification === true ? renderRequestVerification() : undefined}
                {renderVerifyRequest()}
              </React.StrictMode>
            );
          } else { return <React.Fragment />; }
        }}
    </Query>
    );
  };

export { vulnsViewComponent as VulnerabilitiesView };
