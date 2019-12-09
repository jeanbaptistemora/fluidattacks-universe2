/* tslint:disable:no-any jsx-no-multiline-js
 * NO-ANY: Disabling this rule is necessary because there are no specific types
 * for functions such as mapStateToProps and mapDispatchToProps used in the
 * redux wrapper of this component
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that defines the headers of the table
*/
import { ApolloError, NetworkStatus } from "apollo-client";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React, { useState } from "react";
import { Mutation, MutationFn, MutationResult, Query, QueryResult } from "react-apollo";
import { ButtonToolbar, Col, Row } from "react-bootstrap";
import { Comparator, textFilter } from "react-bootstrap-table2-filter";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { AnyAction, Reducer } from "redux";
import { submit } from "redux-form";
import { ThunkDispatch } from "redux-thunk";
import { StateType } from "typesafe-actions";
import { Button } from "../../../../components/Button/index";
import { ConfirmDialog } from "../../../../components/ConfirmDialog/index";
import { DataTableNext } from "../../../../components/DataTableNext";
import { approveFormatter, deleteFormatter, statusFormatter } from "../../../../components/DataTableNext/formatters";
import { IHeader } from "../../../../components/DataTableNext/types";
import { FluidIcon } from "../../../../components/FluidIcon";
import { Modal } from "../../../../components/Modal/index";
import store from "../../../../store/index";
import { hidePreloader, showPreloader } from "../../../../utils/apollo";
import { handleGraphQLErrors } from "../../../../utils/formatHelpers";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import reduxWrapper from "../../../../utils/reduxWrapper";
import translate from "../../../../utils/translations/translate";
import { isValidVulnsFile } from "../../../../utils/validations";
import * as actions from "../../actions";
import { FileInput } from "../../components/FileInput/index";
import TreatmentFieldsView from "../../components/treatmentFields";
import * as actionTypes from "../../containers/DescriptionView/actionTypes";
import { IDescriptionViewProps } from "../../containers/DescriptionView/index";
import { deleteVulnerabilityModal as DeleteVulnerabilityModal } from "../DeleteVulnerability/index";
import { IDeleteVulnAttr } from "../DeleteVulnerability/types";
import { GenericForm } from "../GenericForm";
import { changeFilterValues } from "./actions";
import { default as style } from "./index.css";
import { APPROVE_VULN_MUTATION, GET_VULNERABILITIES, UPDATE_TREATMENT_MUTATION } from "./queries";
import { IApproveVulnAttr, IUpdateTreatmentVulnAttr, IUpdateVulnTreatment,
  IVulnerabilitiesViewProps, IVulnRow, IVulnsAttr, IVulnType } from "./types";

type ISelectRowType = (Array<{[value: string]: string | undefined | null}>);
interface ICategoryVulnType {
  acceptanceDate: string;
  externalBts: string;
  id: string;
  severity: string;
  specific: string;
  tag: string;
  treatment: string;
  treatmentJustification: string;
  treatmentManager: string;
  where: string;
}
interface IVunlDataType {
  id: string;
  treatments: {
    acceptanceDate: string;
    btsUrl: string;
    severity: string;
    tag: string;
    treatment: string;
    treatmentJustification: string;
    treatmentManager: string;

  };
}

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

const groupSpecific: ((lines: IVulnType) => IVulnType) = (lines: IVulnType): IVulnType => {
  const groups: { [key: string]: IVulnType }  = _.groupBy(lines, "where");
  const specificGrouped: IVulnType = _.map(groups, (line: IVulnType) =>
    ({
        acceptanceDate: "",
        analyst: "",
        currentApprovalStatus: line[0].currentApprovalStatus,
        currentState: line[0].currentState,
        externalBts: line[0].externalBts,
        id: line[0].id,
        isNew: line[0].isNew,
        lastAnalyst: "",
        lastApprovedStatus: line[0].lastApprovedStatus,
        severity: "",
        specific: line[0].vulnType === "inputs" ? line.map(getSpecific)
          .join(", ") : groupValues(line.map(specificToNumber)),
        tag: "",
        treatment: line[0].treatment,
        treatmentJustification: line[0].treatmentJustification,
        treatmentManager: line[0].treatmentManager,
        vulnType: line[0].vulnType,
        where: line[0].where,
    }));

  return specificGrouped;
};

const newVulnerabilities: ((lines: IVulnType) => IVulnType) = (lines: IVulnType): IVulnType => (
    _.map(lines, (line: IVulnType[0]) =>
      ({
        acceptanceDate: line.acceptanceDate,
        analyst: line.analyst,
        currentApprovalStatus: line.currentApprovalStatus,
        currentState: line.currentState,
        externalBts: line.externalBts,
        id: line.id,
        isNew: _.isEmpty(line.lastApprovedStatus) ?
        translate.t("search_findings.tab_description.new") :
        translate.t("search_findings.tab_description.old"),
        lastAnalyst: "",
        lastApprovedStatus: line.lastApprovedStatus,
        severity: line.severity,
        specific: line.specific,
        tag: line.tag,
        treatment: line.treatment,
        treatmentJustification: line.treatmentJustification,
        treatmentManager: line.treatmentManager,
        vulnType: line.vulnType,
        where: line.where,
      })));

const updateVulnerabilities: ((findingId: string) => void) = (findingId: string): void => {
  if (isValidVulnsFile("#vulnerabilities")) {
    const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, {}, AnyAction>
    );
    thunkDispatch(actions.updateVulnerabilities(findingId));
  }
};

const getVulnByRow: (selectedRow: ISelectRowType, categoryVuln: ICategoryVulnType[], vulnData: IVunlDataType[]) =>
  IVunlDataType[] = (selectedRow: ISelectRowType, categoryVuln: ICategoryVulnType[], vulnData: IVunlDataType[]):
  IVunlDataType[] => {
    selectedRow.forEach((row: {[value: string]: string | null | undefined }) => {
      categoryVuln.forEach((vuln: {
        acceptanceDate: string;
        externalBts: string;
        id: string;
        severity: string;
        specific: string;
        tag: string;
        treatment: string;
        treatmentJustification: string;
        treatmentManager: string;
        where: string;
      }) => {
        if (row.where === vuln.where && row.specific === vuln.specific) {
        vulnData.push({
          id: vuln.id,
          treatments: {
            acceptanceDate: vuln.acceptanceDate,
            btsUrl: vuln.externalBts,
            severity: vuln.severity,
            tag: vuln.tag,
            treatment: vuln.treatment,
            treatmentJustification: vuln.treatmentJustification,
            treatmentManager: vuln.treatmentManager,
          },
        });
        }
      });
    });

    return vulnData;
  };

const getVulnInfo: (selectedRowArray: ISelectRowType [], arrayVulnCategory: ICategoryVulnType[][]) =>
  IVunlDataType[] = (selectedRowArray: ISelectRowType [], arrayVulnCategory: ICategoryVulnType[][]):
  IVunlDataType[] => {
  let arrayVulnInfo: IVunlDataType[] = [];
  selectedRowArray.forEach((selectedRow: ISelectRowType) => {
    if (!_.isUndefined(selectedRow)) {
      arrayVulnCategory.forEach((category: ICategoryVulnType[]) => {
        arrayVulnInfo = getVulnByRow(selectedRow, category, arrayVulnInfo);
      });
    }
  });

  return arrayVulnInfo;
  };

export const renderButtonBar: ((props: IVulnerabilitiesViewProps) => JSX.Element) =
  (props: IVulnerabilitiesViewProps): JSX.Element => {
    let baseUrl: string; baseUrl = `${window.location.href.split("/dashboard#!")[0]}`;
    const handleUploadVulnerabilities: (() => void) = (): void => {
      updateVulnerabilities(props.findingId);
    };

    return (
      <React.Fragment>
        <Row>
          <Col md={4} sm={12}>
            <Button bsStyle="warning" href={`${baseUrl}/${props.findingId}/download_vulnerabilities`}>
              <FluidIcon icon="export" /> {translate.t("search_findings.tab_description.download_vulnerabilities")}
            </Button>
          </Col>
          <Col md={5} sm={12}>
            <FileInput icon="search" id="vulnerabilities" type=".yaml, .yml" visible={true} />
          </Col>
          <Col md={3} sm={12}>
            <Button bsStyle="success" onClick={handleUploadVulnerabilities}>
              <FluidIcon icon="import" /> {translate.t("search_findings.tab_description.update_vulnerabilities")}
            </Button>
          </Col>
        </Row>
      </React.Fragment>
    );
  };

const vulnsViewComponent: React.FC<IVulnerabilitiesViewProps> =
  (props: IVulnerabilitiesViewProps): JSX.Element => {
    const [modalHidden, setModalHidden] = useState(false);
    const [deleteVulnModal, setDeleteVulnModal] = useState(false);
    const [vulnerabilityId, setVulnerabilityId] = useState("");
    const [filterValueInputs, setFilterValueInputs] = useState("");
    const [filterValueLines, setFilterValueLines] = useState("");
    const [filterValuePorts, setFilterValuePorts] = useState("");
    const emptyArray: string[] = [];
    const [arraySelectedRows, setArraySelectedRows] = useState(emptyArray);
    const [originalProps, setOriginalProps] = useState();

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
    const separatedRow: boolean = !_.isUndefined(props.separatedRow) ? props.separatedRow
    : false;
    const getAnalyst: boolean = !_.isUndefined(props.analyst) ? props.analyst : false;
    const shouldGroup: boolean = !(props.editMode && separatedRow);

    const handleOpenVulnSetClick: () => void = (): void => {
      setModalHidden(true);
    };

    const handleCloseTableSetClick: () => void = (): void => {
      setModalHidden(false);
      if (!_.isUndefined(props.descriptParam)) {
        store.dispatch({
          payload: {
            descriptionData: {...originalProps},
          },
          type: actionTypes.LOAD_DESCRIPTION,
        });
      }
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

    const handleGetVulnerabilities: ((data: IVulnsAttr) => void) = (data: IVulnsAttr): void => {
      if (!_.isUndefined(data)) {
        if (props.vulnerabilities !== undefined) {
          setFilterValueInputs(props.vulnerabilities.filters.filterInputs);
          setFilterValueLines(props.vulnerabilities.filters.filterLines);
          setFilterValuePorts(props.vulnerabilities.filters.filterPorts);
        }
      }
    };

    return(
    <Query
      query={GET_VULNERABILITIES}
      variables={{ identifier: props.findingId, analystField: isAnalystorAdmin }}
      notifyOnNetworkStatusChange={true}
      onCompleted={handleGetVulnerabilities}
    >
      {
        ({loading, error, data, refetch, networkStatus}: QueryResult<IVulnsAttr>): React.ReactNode => {
          const isRefetching: boolean = networkStatus === NetworkStatus.refetch;
          if (loading || isRefetching) {
            showPreloader();

            return <React.Fragment/>;
          }
          if (!_.isUndefined(error)) {
            hidePreloader();
            handleGraphQLErrors("An error occurred getting vulnerabilities", error);

            return <React.Fragment/>;
          }
          if (!_.isUndefined(data)) {
            hidePreloader();

            const dataInputs: IVulnsAttr["finding"]["inputsVulns"] = filterState(
              data.finding.inputsVulns, props.state);
            const dataLines: IVulnsAttr["finding"]["linesVulns"] = filterState(data.finding.linesVulns, props.state);
            const dataPorts: IVulnsAttr["finding"]["portsVulns"] = filterState(data.finding.portsVulns, props.state);
            const dataPendingVulns: IVulnsAttr["finding"]["pendingVulns"] = newVulnerabilities(filterApprovalStatus(
              data.finding.pendingVulns, props.state));

            const handleMtDeleteVulnRes: ((mtResult: IDeleteVulnAttr) => void) = (mtResult: IDeleteVulnAttr): void => {
              if (!_.isUndefined(mtResult)) {
                if (mtResult.deleteVulnerability.success) {
                  setDeleteVulnModal(false);
                  refetch()
                    .catch();
                  hidePreloader();
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
                  hidePreloader();
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
                  hidePreloader();
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

            const handleUpdateTreatError: ((updateError: ApolloError) => void) = (updateError: ApolloError): void => {
              hidePreloader();
              msgError(translate.t("proj_alerts.error_textsad"));

            };
            const handleMtUpdateTreatmentVulnRes: ((mtResult: IUpdateVulnTreatment) => void) =
            (mtResult: IUpdateVulnTreatment): void => {
              if (!_.isUndefined(mtResult)) {
                if (mtResult.updateTreatmentVuln.success) {
                  refetch()
                    .catch();
                  hidePreloader();
                  mixpanel.track(
                    "UpdatedTreatmentVulnerabilities",
                    {
                      Organization: (window as typeof window & { userOrganization: string }).userOrganization,
                      User: (window as typeof window & { userName: string }).userName,
                    });
                  msgSuccess(
                    translate.t("search_findings.tab_description.update_vulnerabilities"),
                    translate.t("proj_alerts.title_success"));
                  handleCloseTableSetClick();
                }
              }
            };
            const onFilterInputs: ((filterVal: string) => void) = (filterVal: string): void => {
              if (props.vulnerabilities !== undefined && filterValueInputs !== filterVal) {
                setFilterValueInputs(filterVal);
                const newValues: {} = {...props.vulnerabilities.filters, filterInputs: filterVal};
                store.dispatch(changeFilterValues(newValues));
              }
            };
            const clearFilterInputs: ((eventInput: any) => void) = (eventInput: any): void => {
              const inputValue: any = document.getElementById(eventInput.target.id);
              if (inputValue.value.length === 0) {
                if (props.vulnerabilities !== undefined && filterValueInputs !== "") {
                  const newValues: {} = {...props.vulnerabilities.filters, filterInputs: ""};
                  store.dispatch(changeFilterValues(newValues));
                }
              }
            };
            const onFilterLines: ((filterVal: string) => void) = (filterVal: string): void => {
              if (props.vulnerabilities !== undefined && filterValueLines !== filterVal) {
                setFilterValueLines(filterVal);
                const newValues: {} = {...props.vulnerabilities.filters, filterLines: filterVal};
                store.dispatch(changeFilterValues(newValues));
              }
            };
            const clearFilterLines: ((eventLine: any) => void) = (eventLine: any): void => {
              const inputValue: any = document.getElementById(eventLine.target.id);
              if (inputValue.value.length === 0) {
                if (props.vulnerabilities !== undefined && filterValueLines !== "") {
                  const newValues: {} = {...props.vulnerabilities.filters, filterLines: ""};
                  store.dispatch(changeFilterValues(newValues));
                }
              }
            };
            const onFilterPorts: ((filterVal: string) => void) = (filterVal: string): void => {
              if (props.vulnerabilities !== undefined && filterValuePorts !== filterVal) {
                setFilterValuePorts(filterVal);
                const newValues: {} = {...props.vulnerabilities.filters, filterPorts: filterVal};
                store.dispatch(changeFilterValues(newValues));
              }
            };
            const clearFilterPorts: ((eventPort: any) => void) = (eventPort: any): void => {
              const inputValue: any = document.getElementById(eventPort.target.id);
              if (inputValue.value.length === 0) {
                if (props.vulnerabilities !== undefined && filterValuePorts !== "") {
                  const newValues: {} = {...props.vulnerabilities.filters, filterPorts: ""};
                  store.dispatch(changeFilterValues(newValues));
                }
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
                defaultValue: props.vulnerabilities !== undefined ? filterValueInputs : "",
                onFilter: onFilterInputs,
                onInput: clearFilterInputs,
              }),
              header: "URL",
              width: "60%",
              wrapped: true,
            },
            {
              align: "left",
              dataField: "specific",
              header: translate.t("search_findings.tab_description.field"),
              width: "20%",
              wrapped: true,
            },
            {
              align: "left",
              dataField: "treatment",
              header: translate.t("search_findings.tab_description.treatment.title"),
              visible: false,
              width: "20%",
            }];
            const linesHeader: IHeader[] = [
              {
                align: "left",
                dataField: "where",
                filter: textFilter({
                  ...columnFilter,
                  defaultValue: props.vulnerabilities !== undefined ? filterValueLines : "",
                  onFilter: onFilterLines,
                  onInput: clearFilterLines,
                }),
                header: translate.t("search_findings.tab_description.path"),
                width: "60%",
                wrapped: true,
              },
              {
                align: "left",
                dataField: "specific",
                header: translate.t("search_findings.tab_description.line", {count: 1}),
                width: "20%",
                wrapped: true,
              },
              {
                align: "left",
                dataField: "treatment",
                header: translate.t("search_findings.tab_description.treatment.title"),
                visible: false,
                width: "20%",
              }];
            const portsHeader: IHeader[] = [
              {
                align: "left",
                dataField: "where",
                filter: textFilter({
                  ...columnFilter,
                  defaultValue: props.vulnerabilities !== undefined ? filterValuePorts : "",
                  onFilter: onFilterPorts,
                  onInput: clearFilterPorts,
                }),
                header: "Host",
                width: "60%",
                wrapped: true,
              },
              {
                align: "left",
                dataField: "specific",
                header: translate.t("search_findings.tab_description.port", {count: 1}),
                width: "20%",
                wrapped: true,
              },
              {
                align: "left",
                dataField: "treatment",
                header: translate.t("search_findings.tab_description.treatment.title"),
                visible: false,
                width: "20%",
              }];

            let formattedDataLines: IVulnsAttr["finding"]["linesVulns"] = dataLines;
            let formattedDataPorts: IVulnsAttr["finding"]["portsVulns"] = dataPorts;
            let formattedDataInputs: IVulnsAttr["finding"]["inputsVulns"] = dataInputs;
            const formattedDataPendingVulns: IVulnsAttr["finding"]["pendingVulns"] = dataPendingVulns;

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
            (): JSX.Element => {
              if (_.isUndefined(originalProps) && !_.isUndefined(props.descriptParam)) {
                setOriginalProps({treatmentManager: props.descriptParam.dataset.treatmentManager});
              }

              return (
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
            };

            const calculateRowsSelected: () => {oneRowSelected: boolean; vulnerabilities: string []} =
            (): {oneRowSelected: boolean; vulnerabilities: string []}  => {
              const selectedRows: Array<NodeListOf<Element>> = getSelectQryTable().selectedQeryArray;
              const selectedRowArray: ISelectRowType[] = [];
              const arrayVulnCategory: ICategoryVulnType[][] = [data.finding.inputsVulns,
                                                                data.finding.linesVulns,
                                                                data.finding.portsVulns];
              let result: {oneRowSelected: boolean; vulnerabilities: string []};
              const vulnsId: string[] = [];
              selectedRows.forEach((selectQry: NodeListOf<Element>) => {
                selectedRowArray.push(getAttrVulnUpdate(selectQry));
              });
              const vulns: IVunlDataType[] = getVulnInfo(selectedRowArray, arrayVulnCategory);
              vulns.forEach((vuln: IVunlDataType) => {
                vulnsId.push(vuln.id);
              });
              result = {
                oneRowSelected: false,
                vulnerabilities: vulnsId,
              };
              if (vulns.length === 1) {
                result = {
                  oneRowSelected: true,
                  vulnerabilities: vulnsId,
                };
                if (!_.isUndefined(props.descriptParam)) {
                  if (modalHidden) {
                    props.descriptParam.formValues.treatmentVuln = props.descriptParam.dataset.treatment.toUpperCase();
                    props.descriptParam.dataset.severity = !_.isEqual(vulns[0].treatments.severity, "-1") ?
                    vulns[0].treatments.severity : "";
                    props.descriptParam.dataset.tag = vulns[0].treatments.tag;
                    props.descriptParam.dataset.treatmentManager = vulns[0].treatments.treatmentManager;
                  }
                }
              }

              return result;
            };

            const numberRowSelected: boolean = calculateRowsSelected().oneRowSelected;
            const vulnsSelected: string [] = calculateRowsSelected().vulnerabilities;

            return (
              <Mutation mutation={APPROVE_VULN_MUTATION} onCompleted={handleMtPendingVulnRes}>
              { (approveVulnerability: MutationFn<IApproveVulnAttr, {
                approvalStatus: boolean; findingId: string; uuid?: string; }>,
                 mutationResult: MutationResult): React.ReactNode => {
                if (mutationResult.loading) {
                  showPreloader();
                }
                if (!_.isUndefined(mutationResult.error)) {
                  hidePreloader();
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

                const openApproveConfirm: (() => void) = (): void => {
                  store.dispatch(actions.openConfirmDialog("confirmApproveVulns"));
                };

                const openDeleteConfirm: (() => void) = (): void => {
                  store.dispatch(actions.openConfirmDialog("confirmDeleteVulns"));
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
                const handleOnSelect: ((row: IVulnRow, isSelect: boolean) => void) =
                (row: IVulnRow, isSelect: boolean): void => {
                  if (isSelect) {
                    const newSet: Set<string> = new Set([...arraySelectedRows, row.id]);
                    setArraySelectedRows(Array.from(newSet));
                  } else {
                    const newSet: Set<string> = new Set(arraySelectedRows.filter((rowId: string) => rowId !== row.id));
                    setArraySelectedRows(Array.from(newSet));
                  }
                };
                const handleOnSelectAll: ((isSelect: boolean, rows: IVulnRow[]) => void) =
                (isSelect: boolean, rows: IVulnRow[]): void => {
                  const newIds: string[] = rows.map((row: IVulnRow) => row.id);
                  if (isSelect) {
                    const newSet: Set<string> = new Set([...arraySelectedRows, ...newIds]);
                    setArraySelectedRows(Array.from(newSet));
                  } else {
                    const newSet: Set<string> = new Set(arraySelectedRows);
                    newIds.forEach((deleteRowId: string) => newSet.delete(deleteRowId));
                    setArraySelectedRows(Array.from(newSet));
                  }
                };
                const selectionMode: SelectRowOptions = {
                  clickToSelect: false,
                  hideSelectColumn: !isEditable,
                  mode: "checkbox",
                  onSelect: handleOnSelect,
                  onSelectAll: handleOnSelectAll,
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
                              exportCsv={false}
                              headers={inputsHeader}
                              onClickRow={undefined}
                              remote={remote}
                              pageSize={10}
                              search={false}
                              title=""
                              selectionMode={selectionMode}
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
                              exportCsv={false}
                              headers={linesHeader}
                              onClickRow={undefined}
                              remote={remote}
                              pageSize={10}
                              search={false}
                              title=""
                              selectionMode={selectionMode}
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
                              exportCsv={false}
                              headers={portsHeader}
                              onClickRow={undefined}
                              remote={remote}
                              pageSize={10}
                              search={false}
                              title=""
                              selectionMode={selectionMode}
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
                          <Button onClick={openApproveConfirm}>
                            <FluidIcon icon="verified" />
                            {translate.t("search_findings.tab_description.approve_all")}
                          </Button>
                          <Button onClick={openDeleteConfirm}>
                            <FluidIcon icon="delete" />
                            {translate.t("search_findings.tab_description.delete_all")}
                          </Button>
                        </ButtonToolbar>
                        : undefined}
                      </React.Fragment>
                      : undefined }
                      <ConfirmDialog
                        name="confirmDeleteVulns"
                        onProceed={handleDeleteAllVulnerabilities}
                        title={translate.t("search_findings.tab_description.delete_all_vulns")}
                      />
                      <ConfirmDialog
                        name="confirmApproveVulns"
                        onProceed={handleApproveAllVulnerabilities}
                        title={translate.t("search_findings.tab_description.approve_all_vulns")}
                      />
                      <DeleteVulnerabilityModal
                        findingId={props.findingId}
                        id={vulnerabilityId}
                        open={deleteVulnModal}
                        onClose={handleCloseDeleteVulnModal}
                        onDeleteVulnRes={handleMtDeleteVulnRes}
                      />

                      <Mutation
                        mutation={UPDATE_TREATMENT_MUTATION}
                        onCompleted={handleMtUpdateTreatmentVulnRes}
                        onError={handleUpdateTreatError}
                      >
                        { (updateTreatmentVuln: MutationFn<IUpdateVulnTreatment, IUpdateTreatmentVulnAttr>,
                           mutationResVuln: MutationResult): React.ReactNode => {
                            if (mutationResVuln.loading) {showPreloader(); }

                            const handleUpdateTreatmentVuln: ((dataTreatment: IDescriptionViewProps["dataset"])
                              => void) = (dataTreatment: IDescriptionViewProps["dataset"]): void => {
                                if (vulnsSelected.length === 0) {
                                    msgError(translate.t("search_findings.tab_resources.no_selection"));
                                } else {
                                  updateTreatmentVuln({variables: {
                                    acceptanceDate: dataTreatment.acceptanceDate,
                                    btsUrl: dataTreatment.btsUrl,
                                    findingId: data.finding.id,
                                    severity: !_.isEmpty(dataTreatment.severity) ? dataTreatment.severity : "-1",
                                    tag: dataTreatment.tag,
                                    treatment: dataTreatment.treatment,
                                    treatmentJustification: dataTreatment.treatmentJustification,
                                    treatmentManager: dataTreatment.treatmentManager,
                                    vulnerabilities: vulnsSelected,
                                  }})
                                  .catch();
                                }
                            };
                            const handleEditTreatment: (() => void) = (): void => {
                              store.dispatch(submit("editTreatmentVulnerability"));
                            };

                            const handleUpdateTreatment: ((values: IDescriptionViewProps["dataset"]) => void) =
                            (values: IDescriptionViewProps["dataset"]): void => {
                              handleUpdateTreatmentVuln(values);
                            };

                            return (
                              <Modal
                                open={modalHidden}
                                footer={
                                  <ButtonToolbar className="pull-right">
                                    <Button onClick={handleCloseTableSetClick}>
                                      {translate.t("project.findings.report.modal_close")}
                                    </Button>
                                    <Button
                                      bsStyle="primary"
                                      onClick={handleEditTreatment}
                                    >
                                      {translate.t("confirmmodal.proceed")}
                                    </Button>
                                  </ButtonToolbar>
                                }
                                headerTitle={translate.t("search_findings.tab_description.editVuln")}
                              >
                              {modalHidden ?
                              <GenericForm
                                name="editTreatmentVulnerability"
                                onSubmit={handleUpdateTreatment}
                                initialValues={
                                  numberRowSelected ? (!_.isUndefined(props.descriptParam) ?
                                  props.descriptParam.dataset : undefined) : undefined
                                }
                              >
                                {!_.isUndefined(props.descriptParam) ?
                                <TreatmentFieldsView isTreatmentModal={true} {...props.descriptParam} />
                                : undefined}
                              </GenericForm>
                              : undefined}
                              </Modal>
                            );
                        }}
                      </Mutation>
                      {isEditable ? renderButtonUpdateVuln() : undefined}
                      {props.editMode && _.includes(["admin", "analyst"], props.userRole)
                        ? renderButtonBar(props)
                        : undefined
                      }
                    </React.StrictMode>
                  );
                }}
              </Mutation>
            );
          }
        }}
    </Query>
    );
  };

const enhance: InferableComponentEnhancer<{}> = lifecycle<IVulnerabilitiesViewProps, {}>({});

const vulnerabilitiesView: React.ComponentType<IVulnerabilitiesViewProps> = reduxWrapper(
  enhance(vulnsViewComponent) as React.FunctionComponent<IVulnerabilitiesViewProps>,
  (state: StateType<Reducer>): IVulnerabilitiesViewProps => ({
    ...state,
    vulnerabilities: state.dashboard.vulnerabilities,
  }),
);

// tslint:disable-next-line: max-file-line-count
export { vulnerabilitiesView as VulnerabilitiesView };
