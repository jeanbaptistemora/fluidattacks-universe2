/* tslint:disable:no-any jsx-no-multiline-js
 * NO-ANY: Disabling this rule is necessary because there are no specific types
 * for functions such as mapStateToProps and mapDispatchToProps used in the
 * redux wrapper of this component
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that defines the headers of the table
*/
import { NetworkStatus } from "apollo-client";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React, { useState } from "react";
import { Mutation, MutationFn, MutationResult, Query, QueryResult } from "react-apollo";
import { ButtonToolbar, Col, Row } from "react-bootstrap";
import { AnyAction } from "redux";
import { submit } from "redux-form";
import { ThunkDispatch } from "redux-thunk";
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
import translate from "../../../../utils/translations/translate";
import { isValidVulnsFile } from "../../../../utils/validations";
import * as actions from "../../actions";
import { FileInput } from "../../components/FileInput/index";
import { TreatmentFieldsView } from "../../components/treatmentFields";
import { IDescriptionViewProps } from "../../containers/DescriptionView/index";
import { deleteVulnerabilityModal as DeleteVulnerabilityModal } from "../DeleteVulnerability/index";
import { IDeleteVulnAttr } from "../DeleteVulnerability/types";
import { GenericForm } from "../GenericForm";
import style from "./index.css";
import { APPROVE_VULN_MUTATION, GET_VULNERABILITIES, UPDATE_TREATMENT_MUTATION } from "./queries";
import { IApproveVulnAttr, IUpdateVulnTreatment, IVulnerabilitiesViewProps, IVulnsAttr, IVulnType } from "./types";

type ISelectRowType = (Array<{[value: string]: string | undefined | null}>);
interface ICategoryVulnType {
  externalBts: string;
  id: string;
  specific: string;
  treatment: string;
  treatmentJustification: string;
  treatmentManager: string;
  where: string;
}
interface IVunlDataType {
  id: string;
  treatments: {
    btsUrl: string;
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

const specificToNumber: ((line: { [key: string]: string }) => number) =
  (line: { [key: string]: string }): number =>
    parseInt(line.specific, 10);

const getSpecific: ((line: { [key: string]: string }) => string) =
  (line: { [key: string]: string }): string =>
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
        analyst: "",
        currentApprovalStatus: line[0].currentApprovalStatus,
        currentState: line[0].currentState,
        externalBts: line[0].externalBts,
        id: line[0].id,
        isNew: line[0].isNew,
        lastAnalyst: "",
        lastApprovedStatus: line[0].lastApprovedStatus,
        specific: line[0].vulnType === "inputs" ? line.map(getSpecific)
          .join(", ") : groupValues(line.map(specificToNumber)),
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
        specific: line.specific,
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
        externalBts: string;
        id: string;
        specific: string;
        treatment: string;
        treatmentJustification: string;
        treatmentManager: string;
        where: string;
      }) => {
        if (row.where === vuln.where && row.specific === vuln.specific) {
        vulnData.push({
          id: vuln.id,
          treatments: {
            btsUrl: vuln.externalBts,
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

    if (!_.isUndefined(props.descriptParam)) {
      props.descriptParam.formValues.treatment = props.descriptParam.formValues.treatmentVuln;
    }
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

    const isEditable: boolean = _.isUndefined(props.renderAsEditable) ? false : props.renderAsEditable;
    const separatedRow: boolean = !_.isUndefined(props.separatedRow) ? props.separatedRow
    : false;
    const getAnalyst: boolean = !_.isUndefined(props.analyst) ? props.analyst : false;
    const shouldGroup: boolean = !(props.editMode && separatedRow);

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

    return(
    <Query
      query={GET_VULNERABILITIES}
      variables={{ identifier: props.findingId, analystField: isAnalystorAdmin }}
      notifyOnNetworkStatusChange={true}
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
            const inputsHeader: IHeader[] = [
            {
              align: "left",
              dataField: "where",
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
              (): JSX.Element =>
                (
                  <React.Fragment>
                    <Row>
                      <Col mdOffset={5} md={4} hidden={true}>
                        <Button bsStyle="warning" onClick={handleOpenVulnSetClick}>
                          <FluidIcon icon="edit" /> {translate.t("search_findings.tab_description.editVuln")}
                        </Button>
                      </Col>
                    </Row><br/>
                </React.Fragment>
              );

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
                  props.descriptParam.dataset.treatment = vulns[0].treatments.treatment.toUpperCase();
                  props.descriptParam.dataset.treatmentJustification = vulns[0].treatments.treatmentJustification;
                  props.descriptParam.dataset.treatmentManager = vulns[0].treatments.treatmentManager;
                  props.descriptParam.dataset.btsUrl = vulns[0].treatments.btsUrl;
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
                const selectionMode: SelectRowOptions = {
                  clickToSelect: true,
                  mode: "checkbox",
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
                              enableRowSelection={
                                ((isEditable ? true : false) && _.includes([], props.userRole))
                              }
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
                              enableRowSelection={
                                ((isEditable ? true : false) && _.includes([], props.userRole))
                              }
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
                              enableRowSelection={
                                ((isEditable ? true : false) && _.includes([], props.userRole))
                              }
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
                          enableRowSelection={false}
                          title=""
                          selectionMode={selectionMode}
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

                      <Mutation mutation={UPDATE_TREATMENT_MUTATION} onCompleted={handleMtUpdateTreatmentVulnRes}>
                        { (updateTreatmentVuln: MutationFn<IUpdateVulnTreatment, {
                         data: {btsUrl: string; findingId: string; treatment: string; treatmentJustification: string;
                                treatmentManager: string; vulnerabilities: string[]; };
                         findingId: string; }>,
                           mutationResVuln: MutationResult): React.ReactNode => {
                            if (mutationResVuln.loading) {showPreloader(); }
                            if (!_.isUndefined(mutationResVuln.error)) {
                              hidePreloader();
                              handleGraphQLErrors("An error occurred updating vulnerabilities",
                                                  mutationResVuln.error);
                              location.reload();

                              return <React.Fragment/>;
                            }

                            const handleUpdateTreatmentVuln: ((dataTreatment: IDescriptionViewProps["dataset"])
                              => void) = (dataTreatment: IDescriptionViewProps["dataset"]): void => {
                              const selectedQry: Array<NodeListOf<Element>> = getSelectQryTable().selectedQeryArray;
                              if (selectedQry.length === 0) {
                                  msgError(translate.t("search_findings.tab_resources.no_selection"));
                                } else {

                                    updateTreatmentVuln({variables: { data: {btsUrl: dataTreatment.btsUrl,
                                                                             findingId: data.finding.id,
                                                                             treatment: dataTreatment.treatment,
                                                                             treatmentJustification:
                                                                             dataTreatment.treatmentJustification,
                                                                             treatmentManager:
                                                                             dataTreatment.treatmentManager,
                                                                             vulnerabilities: vulnsSelected },
                                                                      findingId: data.finding.id}})
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
                                footer={undefined}
                                headerTitle={translate.t("search_findings.tab_description.editVuln")}
                              >
                              <GenericForm
                                name="editTreatmentVulnerability"
                                onSubmit={handleUpdateTreatment}
                                initialValues={
                                  numberRowSelected ? (!_.isUndefined(props.descriptParam) ?
                                  props.descriptParam.dataset : undefined) : undefined
                                }
                              >
                                {!_.isUndefined(props.descriptParam) ?
                                TreatmentFieldsView(props.descriptParam)
                                : undefined}
                                  <ButtonToolbar className="pull-right">
                                    <Button
                                      bsStyle="primary"
                                      onClick={handleEditTreatment}
                                    >
                                      {translate.t("confirmmodal.proceed")}
                                    </Button>
                                    <Button onClick={handleCloseTableSetClick}>
                                      {translate.t("project.findings.report.modal_close")}
                                    </Button>
                                  </ButtonToolbar>
                              </GenericForm>
                              </Modal>
                            );
                        }}
                      </Mutation>
                      {props.editMode && _.includes(["customer"], props.userRole)
                        ? renderButtonUpdateVuln()
                        : undefined
                      }
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

export { vulnsViewComponent as VulnerabilitiesView };
