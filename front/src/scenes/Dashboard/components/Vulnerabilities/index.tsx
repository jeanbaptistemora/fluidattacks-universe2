/* tslint:disable: jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that defines the headers of the table
*/
import { MutationFunction, MutationResult, QueryResult } from "@apollo/react-common";
import { Mutation, Query } from "@apollo/react-components";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React, { useState } from "react";
import { ButtonToolbar, Col, Row } from "react-bootstrap";
import { Comparator, textFilter } from "react-bootstrap-table2-filter";
import { Button } from "../../../../components/Button/index";
import { ConfirmDialog, ConfirmFn } from "../../../../components/ConfirmDialog/index";
import { DataTableNext } from "../../../../components/DataTableNext";
import { approveFormatter, deleteFormatter, statusFormatter } from "../../../../components/DataTableNext/formatters";
import { IHeader } from "../../../../components/DataTableNext/types";
import { FluidIcon } from "../../../../components/FluidIcon";
import { handleGraphQLErrors } from "../../../../utils/formatHelpers";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import translate from "../../../../utils/translations/translate";
import { deleteVulnerabilityModal as DeleteVulnerabilityModal } from "../DeleteVulnerability/index";
import { IDeleteVulnAttr } from "../DeleteVulnerability/types";
import { default as style } from "./index.css";
import { APPROVE_VULN_MUTATION, GET_VULNERABILITIES } from "./queries";
import {
  IApproveVulnAttr, IVulnDataType, IVulnerabilitiesViewProps, IVulnRow, IVulnsAttr, IVulnType,
} from "./types";
import { UpdateTreatmentModal } from "./updateTreatment";
import { UploadVulnerabilites } from "./uploadFile";

type ISelectRowType = (Array<{[value: string]: string | undefined | null}>);

export const getAttrVulnUpdate: (selectedQery: NodeListOf<Element>) => ISelectRowType =
(selectedQery: NodeListOf<Element>): ISelectRowType =>  {
  const attrVuln: ISelectRowType = [];
  selectedQery.forEach((element: Element) => {
    if (element.className !== "react-bs-select-all") {
      const selectedRow: HTMLTableRowElement | null = element.closest("tr");
      attrVuln.push ({
        specific: _.isNull(selectedRow) ? undefined : selectedRow.children[2].textContent,
        where: _.isNull(selectedRow) ? undefined : selectedRow.children[1].textContent,
        });
      }
    },
  );

  return attrVuln;
};

const filterApprovalStatus:
  ((dataVuln: IVulnType, state: string) => IVulnType) =
    (dataVuln: IVulnType, state: string): IVulnType =>

      dataVuln.filter((vuln: IVulnType[0]) => vuln.currentApprovalStatus === state);

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

const getVulnByRow: (selectedRow: ISelectRowType, categoryVuln: IVulnRow[], vulnData: IVulnDataType[]) =>
  IVulnDataType[] = (selectedRow: ISelectRowType, categoryVuln: IVulnRow[], vulnData: IVulnDataType[]):
  IVulnDataType[] => {
    selectedRow.forEach((row: {[value: string]: string | null | undefined }) => {
      categoryVuln.forEach((vuln: {
        currentState: string;
        id: string;
        severity: string;
        specific: string;
        tag: string;
        treatmentManager: string;
        where: string;
      }) => {
        if (row.where === vuln.where && row.specific === vuln.specific) {
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
    });

    return vulnData;
  };

const getVulnInfo: (selectedRowArray: ISelectRowType [], arrayVulnCategory: IVulnRow[][]) =>
  IVulnDataType[] = (selectedRowArray: ISelectRowType [], arrayVulnCategory: IVulnRow[][]):
  IVulnDataType[] => {
  let arrayVulnInfo: IVulnDataType[] = [];
  selectedRowArray.forEach((selectedRow: ISelectRowType) => {
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
    const [modalHidden, setModalHidden] = useState(false);
    const [deleteVulnModal, setDeleteVulnModal] = useState(false);
    const [vulnerabilityId, setVulnerabilityId] = useState("");
    const emptyArray: string[] = [];
    const [arraySelectedRows, setArraySelectedRows] = useState(emptyArray);
    const [selectRowsInputs, setSelectRowsInputs] = useState<number[]>([]);
    const [selectRowsLines, setSelectRowsLines] = useState<number[]>([]);
    const [selectRowsPorts, setSelectRowsPorts] = useState<number[]>([]);

    const isAnalystorAdmin: boolean = _.includes(["analyst", "admin"], props.userRole);

    const getSelectQryTable: () => {selectedQeryArray: Array<NodeListOf<Element>> } = ():
      { selectedQeryArray: Array<NodeListOf<Element>> } => {
      const selectedQryArray: Array<NodeListOf<Element>> = [];
      const vulnsTable: string[] = ["#inputsVulns", "#linesVulns", "#portsVulns"];
      vulnsTable.forEach((table: string) => {
        const qryTable: NodeListOf<Element> = document.querySelectorAll(`${table} tr input:checked`);
        if (!_.isEmpty(qryTable)) {
          selectedQryArray.push(qryTable);
        }
      });
      const result: { selectedQeryArray: Array<NodeListOf<Element>> } = {
        selectedQeryArray: selectedQryArray,
      };

      return result;
    };
    const isEditable: boolean = props.editMode && _.includes(["customer", "customeradmin"], props.userRole);
    const canRequestVerification: boolean =  props.isRequestVerification === true
      && _.includes(["customer", "customeradmin"], props.userRole);
    const canVerifyRequest: boolean =  props.isVerifyRequest === true
      && _.includes(["admin", "analyst"], props.userRole);
    const hideSelectionColumn: boolean = !(isEditable || canRequestVerification || canVerifyRequest);
    const separatedRow: boolean = !_.isUndefined(props.separatedRow) ? props.separatedRow
    : false;
    const getAnalyst: boolean = !_.isUndefined(props.analyst) ? props.analyst : false;
    const shouldGroup: boolean = !(props.editMode && separatedRow) && !(canRequestVerification || canVerifyRequest);

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

    return(
    <Query
      query={GET_VULNERABILITIES}
      variables={{ identifier: props.findingId, analystField: false }}
    >
      {
        ({ error, data, refetch }: QueryResult<IVulnsAttr>): JSX.Element => {
          if (_.isUndefined(data) || _.isEmpty(data)) {

            return <React.Fragment/>;
          }
          if (!_.isUndefined(error)) {
            handleGraphQLErrors("An error occurred getting vulnerabilities", error);

            return <React.Fragment/>;
          }
          if (!_.isUndefined(data)) {

            const dataInputs: IVulnsAttr["finding"]["inputsVulns"] = newVulnerabilities(filterState(
              data.finding.inputsVulns, props.state));
            const dataLines: IVulnsAttr["finding"]["linesVulns"] = newVulnerabilities(filterState(
              data.finding.linesVulns, props.state));
            const dataPorts: IVulnsAttr["finding"]["portsVulns"] = newVulnerabilities(filterState(
              data.finding.portsVulns, props.state));
            const dataPendingVulns: IVulnsAttr["finding"]["pendingVulns"] = newVulnerabilities(filterApprovalStatus(
              data.finding.pendingVulns, props.state));

            const handleMtDeleteVulnRes: ((mtResult: IDeleteVulnAttr) => void) = (mtResult: IDeleteVulnAttr): void => {
              if (!_.isUndefined(mtResult)) {
                if (mtResult.deleteVulnerability.success) {
                  setDeleteVulnModal(false);
                  refetch()
                    .catch();
                  mixpanel.track(
                    "DeleteVulnerability",
                    {
                      Organization: (window as typeof window & { userOrganization: string }).userOrganization,
                      User: (window as typeof window & { userName: string }).userName,
                    });
                  msgSuccess(
                    translate.t("search_findings.tab_description.vulnDeleted"),
                    translate.t("proj_alerts.title_success"));
                } else {
                  msgError(
                    translate.t("delete_vulns.not_success"),
                  );
                  setDeleteVulnModal(false);
                }
              }
            };

            const handleMtPendingVulnRes: ((mtResult: IApproveVulnAttr) => void) = (mtResult: IApproveVulnAttr):
            void => {
              if (!_.isUndefined(mtResult)) {
                if (mtResult.approveVulnerability.success) {
                  refetch()
                    .catch();
                  mixpanel.track(
                    "ApproveVulnerability",
                    {
                      Organization: (window as typeof window & { userOrganization: string }).userOrganization,
                      User: (window as typeof window & { userName: string }).userName,
                    });
                  msgSuccess(
                    translate.t("search_findings.tab_description.vuln_approval"),
                    translate.t("proj_alerts.title_success"));
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
            const clearFilterInputs: ((event: React.FormEvent<HTMLInputElement>) => void) = (
              event: React.FormEvent<HTMLInputElement>,
            ): void => {
              const inputValue: string = event.currentTarget.value;
              if (inputValue.length === 0) {
                sessionStorage.removeItem("vulnInputsFilter");
              }
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
            const clearFilterLines: ((event: React.FormEvent<HTMLInputElement>) => void) = (
              event: React.FormEvent<HTMLInputElement>,
            ): void => {
              const inputValue: string = event.currentTarget.value;
              if (inputValue.length === 0) {
                sessionStorage.removeItem("vulnLinesFilter");
              }
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
            const clearFilterPorts: ((event: React.FormEvent<HTMLInputElement>) => void) = (
              event: React.FormEvent<HTMLInputElement>,
            ): void => {
              const inputValue: string = event.currentTarget.value;
              if (inputValue.length === 0) {
                sessionStorage.removeItem("vulnPortsFilter");
              }
            };
            const columnFilter: TextFilterProps = {
              className: style.filter_input,
              comparator: Comparator.LIKE,
              delay: 1000,
            };
            const inputsHeader: IHeader[] = [
            {
              align: "left",
              dataField: "where",
              filter: textFilter({
                ...columnFilter,
                defaultValue: _.get(sessionStorage, "vulnInputsFilter"),
                onFilter: onFilterInputs,
                onInput: clearFilterInputs,
              }),
              header: "URL",
              onSort: onSortInputs,
              width: "60%",
              wrapped: true,
            },
            {
              align: "left",
              dataField: "specific",
              header: translate.t("search_findings.tab_description.field"),
              onSort: onSortInputs,
              width: "20%",
              wrapped: true,
            }];
            const linesHeader: IHeader[] = [
              {
                align: "left",
                dataField: "where",
                filter: textFilter({
                  ...columnFilter,
                  defaultValue: _.get(sessionStorage, "vulnLinesFilter"),
                  onFilter: onFilterLines,
                  onInput: clearFilterLines,
                }),
                header: translate.t("search_findings.tab_description.path"),
                onSort: onSortLines,
                width: "60%",
                wrapped: true,
              },
              {
                align: "left",
                dataField: "specific",
                header: translate.t("search_findings.tab_description.line", {count: 1}),
                onSort: onSortLines,
                width: "20%",
                wrapped: true,
              }];
            const portsHeader: IHeader[] = [
              {
                align: "left",
                dataField: "where",
                filter: textFilter({
                  ...columnFilter,
                  defaultValue: _.get(sessionStorage, "vulnPortsFilter"),
                  onFilter: onFilterPorts,
                  onInput: clearFilterPorts,
                }),
                header: "Host",
                onSort: onSortPorts,
                width: "60%",
                wrapped: true,
              },
              {
                align: "left",
                dataField: "specific",
                header: translate.t("search_findings.tab_description.port", {count: 1}),
                onSort: onSortPorts,
                width: "20%",
                wrapped: true,
              }];

            let formattedDataLines: IVulnsAttr["finding"]["linesVulns"] = dataLines;
            let formattedDataPorts: IVulnsAttr["finding"]["portsVulns"] = dataPorts;
            let formattedDataInputs: IVulnsAttr["finding"]["inputsVulns"] = dataInputs;
            const formattedDataPendingVulns: IVulnsAttr["finding"]["pendingVulns"] = dataPendingVulns;

            if (props.state !== "PENDING") {
              inputsHeader.push(
                {
                  align: "left",
                  dataField: "verification",
                  formatter: statusFormatter,
                  header: translate.t("search_findings.tab_description.verification"),
                  onSort: onSortInputs,
                  width: "20%",
                },
                {
                  align: "left",
                  dataField: "tag",
                  header: translate.t("search_findings.tab_description.tag"),
                  onSort: onSortInputs,
                  visible: true,
                  width: "20%",
                },
                {
                  align: "left",
                  dataField: "severity",
                  header: translate.t("search_findings.tab_description.business_criticality"),
                  onSort: onSortInputs,
                  visible: true,
                  width: "25%",
                },
                {
                  align: "left",
                  dataField: "treatmentManager",
                  header: translate.t("search_findings.tab_description.treatment_mgr"),
                  onSort: onSortInputs,
                  visible: true,
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
                  width: "20%",
                },
                {
                  align: "left",
                  dataField: "tag",
                  header: translate.t("search_findings.tab_description.tag"),
                  onSort: onSortLines,
                  visible: true,
                  width: "20%",
                },
                {
                  align: "left",
                  dataField: "severity",
                  header: translate.t("search_findings.tab_description.business_criticality"),
                  onSort: onSortLines,
                  visible: true,
                  width: "25%",
                },
                {
                  align: "left",
                  dataField: "treatmentManager",
                  header: translate.t("search_findings.tab_description.treatment_mgr"),
                  onSort: onSortLines,
                  visible: true,
                  width: "30%",
                },
              );
              portsHeader.push(
                {
                  align: "left",
                  dataField: "verification",
                  formatter: statusFormatter,
                  header: translate.t("search_findings.tab_description.verification"),
                  onSort: onSortPorts,
                  width: "20%",
                },
                {
                  align: "left",
                  dataField: "tag",
                  header: translate.t("search_findings.tab_description.tag"),
                  onSort: onSortPorts,
                  visible: true,
                  width: "20%",
                },
                {
                  align: "left",
                  dataField: "severity",
                  header: translate.t("search_findings.tab_description.business_criticality"),
                  onSort: onSortPorts,
                  visible: true,
                  width: "25%",
                },
                {
                  align: "left",
                  dataField: "treatmentManager",
                  header: translate.t("search_findings.tab_description.treatment_mgr"),
                  onSort: onSortPorts,
                  visible: true,
                  width: "30%",
                },
              );
            }

            if (props.editMode && isAnalystorAdmin) {
              inputsHeader.push({
                          align: "center",
                          dataField: "id",
                          deleteFunction: handleDeleteVulnerability,
                          formatter: deleteFormatter,
                          header: translate.t("search_findings.tab_description.action"),
                          width: "10%",
                        });
              linesHeader.push({
                          align: "center",
                          dataField: "id",
                          deleteFunction: handleDeleteVulnerability,
                          formatter: deleteFormatter,
                          header: translate.t("search_findings.tab_description.action"),
                          width: "10%",
                        });
              portsHeader.push({
                          align: "center",
                          dataField: "id",
                          deleteFunction: handleDeleteVulnerability,
                          formatter: deleteFormatter,
                          header: translate.t("search_findings.tab_description.action"),
                          width: "10%",
                        });
            } else if (getAnalyst) {
              inputsHeader.push({
                align: "left",
                dataField: "lastAnalyst",
                header: translate.t("search_findings.tab_description.analyst"),
                width: "30%",
              });
              linesHeader.push({
                align: "left",
                dataField: "lastAnalyst",
                header: translate.t("search_findings.tab_description.analyst"),
                width: "30%",
              });
              portsHeader.push({
                align: "left",
                dataField: "lastAnalyst",
                header: translate.t("search_findings.tab_description.analyst"),
                width: "30%",
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
                          bsStyle="warning"
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
              const selectedRows: Array<NodeListOf<Element>> = getSelectQryTable().selectedQeryArray;
              const selectedRowArray: ISelectRowType[] = [];
              const arrayVulnCategory: IVulnRow[][] = [
                data.finding.inputsVulns,
                data.finding.linesVulns,
                data.finding.portsVulns,
              ];
              selectedRows.forEach((selectQry: NodeListOf<Element>) => {
                selectedRowArray.push(getAttrVulnUpdate(selectQry));
              });
              const vulns: IVulnDataType[] = getVulnInfo(selectedRowArray, arrayVulnCategory);

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
                  {canRequestVerification ?
                    <Row>
                      <Col mdOffset={5} md={4}>
                        <Button
                          id="request_verification_vulns"
                          bsStyle="success"
                          onClick={handleClick}
                          disabled={!(arraySelectedRows.length > 0)}
                        >
                          <FluidIcon icon="verified" /> {translate.t("search_findings.tab_description.request_verify")}
                        </Button>
                      </Col><br/>
                    </Row>
                  : undefined}
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
                  {canVerifyRequest ?
                    <Row>
                      <Col mdOffset={5} md={4}>
                        <Button
                          bsStyle="success"
                          onClick={handleClick}
                          disabled={!(arraySelectedRows.length > 0)}
                        >
                          <FluidIcon icon="verified" /> {translate.t("search_findings.tab_description.mark_verified")}
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

            return (
              <Mutation mutation={APPROVE_VULN_MUTATION} onCompleted={handleMtPendingVulnRes}>
              { (approveVulnerability: MutationFunction<IApproveVulnAttr, {
                approvalStatus: boolean; findingId: string; uuid?: string; }>,
                 mutationResult: MutationResult): JSX.Element => {
                if (!_.isUndefined(mutationResult.error)) {
                  handleGraphQLErrors("An error occurred approving vulnerabilities", mutationResult.error);

                  return <React.Fragment/>;
                }

                const handleApproveVulnerability: ((vulnInfo: { [key: string]: string } | undefined) =>
                void) =
                  (vulnInfo: { [key: string]: string } | undefined): void => {
                    if (vulnInfo !== undefined) {
                      approveVulnerability({ variables: {approvalStatus: true, findingId: props.findingId,
                                                         uuid: vulnInfo.id}})
                      .catch();
                    }
                };
                const handleRejectVulnerability: ((vulnInfo: { [key: string]: string } | undefined) =>
                void) =
                  (vulnInfo: { [key: string]: string } | undefined): void => {
                    if (vulnInfo !== undefined) {
                      approveVulnerability({ variables: {approvalStatus: false, findingId: props.findingId,
                                                         uuid: vulnInfo.id}})
                      .catch();
                    }
                };

                const handleApproveAllVulnerabilities: (() => void) = (): void => {
                  approveVulnerability({ variables: {approvalStatus: true, findingId: props.findingId }})
                  .catch();
                };

                const handleDeleteAllVulnerabilities: (() => void) = (): void => {
                  approveVulnerability({ variables: {approvalStatus: false, findingId: props.findingId }})
                  .catch();
                };

                const pendingsHeader: IHeader[] = [
                  {
                    align: "left",
                    dataField: "where",
                    header: "Where",
                    width: "50%",
                    wrapped: true,
                  },
                  {
                    align: "left",
                    dataField: "specific",
                    header: translate.t("search_findings.tab_description.field"),
                    width: "15%",
                    wrapped: true,
                  },
                  {
                    align: "left",
                    dataField: "currentState",
                    formatter: statusFormatter,
                    header: translate.t("search_findings.tab_description.state"),
                    width: "15%",
                    wrapped: true,
                  },
                  {
                    align: "left",
                    dataField: "isNew",
                    header: translate.t("search_findings.tab_description.is_new"),
                    width: "12%",
                    wrapped: true,
                  }];
                if (getAnalyst) {
                  pendingsHeader.push({
                    align: "left",
                    dataField: "analyst",
                    header: translate.t("search_findings.tab_description.analyst"),
                    width: "38%",
                  });
                }
                if (_.isEqual(props.editModePending, true)) {
                  pendingsHeader.push({
                    align: "center",
                    approveFunction: handleApproveVulnerability,
                    dataField: "id",
                    formatter: approveFormatter,
                    header: translate.t("search_findings.tab_description.approve"),
                    width: "12%",
                  });
                  pendingsHeader.push({
                    align: "center",
                    dataField: "id",
                    deleteFunction: handleRejectVulnerability,
                    formatter: deleteFormatter,
                    header: translate.t("search_findings.tab_description.delete"),
                    width: "12%",
                  });
                  }
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
                    setSelectRowsInputs([...newArray]);
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
                    setSelectRowsLines([...newArray]);
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
                    setSelectRowsPorts([...newArray]);
                  } else {
                    const newSet: Set<string> = new Set(arraySelectedRows);
                    newIds.forEach((deleteRowId: string) => newSet.delete(deleteRowId));
                    setArraySelectedRows(Array.from(newSet));
                    setSelectRowsPorts([]);
                  }
                };
                const selectionModeInputs: SelectRowOptions = {
                  clickToSelect: false,
                  hideSelectColumn: hideSelectionColumn,
                  mode: "checkbox",
                  nonSelectable: props.isRequestVerification === true ? inputVulnsRemediated :
                  props.isVerifyRequest === true ? inputVulnsVerified : undefined,
                  onSelect: handleOnSelectInputs,
                  onSelectAll: handleOnSelectAllInputs,
                  selected: selectRowsInputs,
                };
                const selectionModeLines: SelectRowOptions = {
                  clickToSelect: false,
                  hideSelectColumn: hideSelectionColumn,
                  mode: "checkbox",
                  nonSelectable: props.isRequestVerification === true ? lineVulnsRemediated :
                  props.isVerifyRequest === true ? lineVulnsVerified : undefined,
                  onSelect: handleOnSelectLines,
                  onSelectAll: handleOnSelectAllLines,
                  selected: selectRowsLines,
                };
                const selectionModePorts: SelectRowOptions = {
                  clickToSelect: false,
                  hideSelectColumn: hideSelectionColumn,
                  mode: "checkbox",
                  nonSelectable: props.isRequestVerification === true ? portVulnsRemediated :
                  props.isVerifyRequest === true ? portVulnsVerified : undefined,
                  onSelect: handleOnSelectPorts,
                  onSelectAll: handleOnSelectAllPorts,
                  selected: selectRowsPorts,
                };
                const remote: RemoteProps = {
                  cellEdit: false,
                  filter: false,
                  pagination: false,
                  sort: false,
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
                              onClickRow={undefined}
                              remote={remote}
                              pageSize={10}
                              search={false}
                              title=""
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
                              onClickRow={undefined}
                              remote={remote}
                              pageSize={10}
                              search={false}
                              title=""
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
                              onClickRow={undefined}
                              remote={remote}
                              pageSize={10}
                              search={false}
                              title=""
                              selectionMode={selectionModePorts}
                              tableBody={style.tableBody}
                              tableHeader={style.tableHeader}
                            />
                          </React.Fragment>
                        : undefined
                      }
                      { dataPendingVulns.length > 0 ?
                      <React.Fragment>
                        <DataTableNext
                          id="pendingVulns"
                          bordered={false}
                          dataset={formattedDataPendingVulns}
                          exportCsv={false}
                          headers={pendingsHeader}
                          onClickRow={undefined}
                          remote={remote}
                          pageSize={10}
                          search={false}
                          title=""
                          tableBody={style.tableBody}
                          tableHeader={style.tableHeader}
                        />
                        {_.includes(["admin", "analyst"], props.userRole) ?
                          <ButtonToolbar className="pull-right">
                            <ConfirmDialog title={translate.t("search_findings.tab_description.approve_all_vulns")}>
                              {(confirm: ConfirmFn): React.ReactNode => {
                                const handleClick: (() => void) = (): void => {
                                  confirm(() => { handleApproveAllVulnerabilities(); });
                                };

                                return (
                                  <Button onClick={handleClick}>
                                    <FluidIcon icon="verified" />
                                    {translate.t("search_findings.tab_description.approve_all")}
                                  </Button>
                                );
                              }}
                            </ConfirmDialog>
                            <ConfirmDialog title={translate.t("search_findings.tab_description.delete_all_vulns")}>
                              {(confirm: ConfirmFn): React.ReactNode => {
                                const handleClick: (() => void) = (): void => {
                                  confirm(() => { handleDeleteAllVulnerabilities(); });
                                };

                                return (
                                  <Button onClick={handleClick}>
                                    <FluidIcon icon="delete" />
                                    {translate.t("search_findings.tab_description.delete_all")}
                                  </Button>
                                );
                              }}
                            </ConfirmDialog>
                          </ButtonToolbar>
                        : undefined}
                      </React.Fragment>
                      : undefined }
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
                          userRole={props.userRole}
                          projectName={props.projectName}
                          vulnerabilities={vulnerabilitiesList}
                          handleCloseModal={handleCloseTableSetClick}
                        />
                      : undefined }
                      {isEditable ? renderButtonUpdateVuln() : undefined}
                      {renderRequestVerification()}
                      {renderVerifyRequest()}
                      {props.editMode && _.includes(["admin", "analyst"], props.userRole)
                        ? <UploadVulnerabilites {...props} />
                        : undefined
                      }
                    </React.StrictMode>
                  );
                }}
              </Mutation>
            );
          } else { return <React.Fragment />; }
        }}
    </Query>
    );
  };

// tslint:disable-next-line: max-file-line-count
export { vulnsViewComponent as VulnerabilitiesView };
