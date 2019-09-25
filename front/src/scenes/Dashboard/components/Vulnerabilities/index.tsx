/* tslint:disable:jsx-no-lambda no-any jsx-no-multiline-js no-empty
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 *
 * NO-ANY: Disabling this rule is necessary because there are no specific types
 * for functions such as mapStateToProps and mapDispatchToProps used in the
 * redux wrapper of this component
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that defines the headers of the table
*/
import { NetworkStatus } from "apollo-boost";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React, { useState } from "react";
import { Mutation, MutationFn, MutationResult, Query, QueryResult } from "react-apollo";
import { ButtonToolbar, Col, Row } from "react-bootstrap";
import { DataAlignType } from "react-bootstrap-table";
import { AnyAction } from "redux";
import { submit } from "redux-form";
import { ThunkDispatch } from "redux-thunk";
import { Button } from "../../../../components/Button/index";
import { IHeader } from "../../../../components/DataTable/index";
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
import { GenericForm } from "../GenericForm";
import { default as SimpleTable } from "../SimpleTable/index";
import style from "./index.css";
import { APPROVE_VULN_MUTATION, DELETE_VULN_MUTATION, GET_VULNERABILITIES,
         UPDATE_TREATMENT_MUTATION } from "./queries";
import { IApproveVulnAttr, IDeleteVulnAttr, IUpdateVulnTreatment, IVulnerabilitiesViewProps,
         IVulnsAttr, IVulnType } from "./types";

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

const groupValues: ((values: number[]) => string) =
  (values: number[]): string =>
    getRanges(values.sort(compareNumbers));

const groupSpecific: ((lines: IVulnType) => IVulnType) = (lines: IVulnType): IVulnType => {
  const groups: { [key: string]: IVulnType }  = _.groupBy(lines, "where");
  const specificGrouped: IVulnType =
  _.map(groups, (line: IVulnType) =>
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

export const renderButtonBar: ((props: IVulnerabilitiesViewProps) => JSX.Element) =
  (props: IVulnerabilitiesViewProps): JSX.Element => {
    let baseUrl: string; baseUrl = `${window.location.href.split("/dashboard#!")[0]}`;

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
            <Button bsStyle="success" onClick={(): void => { updateVulnerabilities(props.findingId); }}>
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

    if (!_.isUndefined(props.descriptParam)) {
      props.descriptParam.formValues.treatment = props.descriptParam.formValues.treatmentVuln;
    }
    const canGetAnalyst: boolean = _.includes(["analyst", "admin"], props.userRole);

    return(
    <Query
      query={GET_VULNERABILITIES}
      variables={{ identifier: props.findingId, analystField: canGetAnalyst }}
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

            const getVulnByRow: (selectedRow: ISelectRowType, categoryVuln: ICategoryVulnType[],
                                 vulnData: IVunlDataType[]) => IVunlDataType[] =
                (selectedRow: ISelectRowType, categoryVuln: ICategoryVulnType[], vulnData: IVunlDataType[])
                                                                    : IVunlDataType[] => {
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
              selectedRowArray.map((selectedRow: ISelectRowType) => {
                if (!_.isUndefined(selectedRow)) {
                  arrayVulnCategory.map((category: ICategoryVulnType[]) => {
                    arrayVulnInfo = getVulnByRow(selectedRow, category, arrayVulnInfo);
                  });
                }
              });

              return arrayVulnInfo;
            };

            const dataInputs: IVulnsAttr["finding"]["inputsVulns"] = filterState(
              data.finding.inputsVulns, props.state);
            const dataLines: IVulnsAttr["finding"]["linesVulns"] = filterState(data.finding.linesVulns, props.state);
            const dataPorts: IVulnsAttr["finding"]["portsVulns"] = filterState(data.finding.portsVulns, props.state);
            const dataPendingVulns: IVulnsAttr["finding"]["pendingVulns"] = newVulnerabilities(filterApprovalStatus(
              data.finding.pendingVulns, props.state));

            const handleMtDeleteVulnRes: ((mtResult: IDeleteVulnAttr) => void) = (mtResult: IDeleteVulnAttr): void => {
              if (!_.isUndefined(mtResult)) {
                if (mtResult.deleteVulnerability.success) {
                  refetch()
                    .catch();
                  hidePreloader();
                  mixpanel.track(
                    "DeleteVulnerability",
                    {
                      Organization: (window as Window & { userOrganization: string }).userOrganization,
                      User: (window as Window & { userName: string }).userName,
                    });
                  msgSuccess(
                    translate.t("search_findings.tab_description.vulnDeleted"),
                    translate.t("proj_alerts.title_success"));
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
                      Organization: (window as Window & { userOrganization: string }).userOrganization,
                      User: (window as Window & { userName: string }).userName,
                    });
                  msgSuccess(
                    translate.t("search_findings.tab_description.vuln_approval"),
                    translate.t("proj_alerts.title_success"));
                }
              }
            };

            const getSelectQryTable: () => {selectedQeryArray: Array<NodeListOf<Element>> } = ():
                { selectedQeryArray: Array<NodeListOf<Element>> } => {
                const selectedQryArray: Array<NodeListOf<Element>> = [];
                const vulnsTable: string[] = ["#inputsVulns", "#linesVulns", "#portsVulns"];
                vulnsTable.map((table: string) => {
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

            return (
              <Mutation mutation={DELETE_VULN_MUTATION} onCompleted={handleMtDeleteVulnRes}>
                { (deleteVulnerability: MutationFn<IDeleteVulnAttr, {findingId: string; id: string}>,
                   mutationRes: MutationResult): React.ReactNode => {
                  if (mutationRes.loading) {
                    showPreloader();
                  }
                  if (!_.isUndefined(mutationRes.error)) {
                    hidePreloader();
                    handleGraphQLErrors("An error occurred deleting vulnerabilities", mutationRes.error);

                    return <React.Fragment/>;
                  }

                  const handleDeleteVulnerability: ((vulnInfo: { [key: string]: string } | undefined) => void) =
                    (vulnInfo: { [key: string]: string } | undefined): void => {
                      if (vulnInfo !== undefined) {
                        deleteVulnerability({ variables: {findingId: vulnInfo.findingId, id: vulnInfo.id}})
                        .catch();
                      }
                  };

                  const inputsHeader: IHeader[] = [
                    {
                      align: "left" as DataAlignType,
                      dataField: "where",
                      header: "URL",
                      isDate: false,
                      isStatus: false,
                      width: "60%",
                      wrapped: true,
                    },
                    {
                      align: "left" as DataAlignType,
                      dataField: "specific",
                      header: translate.t("search_findings.tab_description.field"),
                      isDate: false,
                      isStatus: false,
                      width: "20%",
                      wrapped: true,
                    },
                    {
                      align: "left" as DataAlignType,
                      dataField: "treatment",
                      header: translate.t("search_findings.tab_description.treatment.title"),
                      isDate: false,
                      isStatus: false,
                      visible: false,
                      width: "20%",
                    }];
                  const linesHeader: IHeader[] = [
                    {
                      align: "left" as DataAlignType,
                      dataField: "where",
                      header: translate.t("search_findings.tab_description.path"),
                      isDate: false,
                      isStatus: false,
                      width: "60%",
                      wrapped: true,
                    },
                    {
                      align: "left" as DataAlignType,
                      dataField: "specific",
                      header: translate.t("search_findings.tab_description.line", {count: 1}),
                      isDate: false,
                      isStatus: false,
                      width: "20%",
                      wrapped: true,
                    },
                    {
                      align: "left" as DataAlignType,
                      dataField: "treatment",
                      header: translate.t("search_findings.tab_description.treatment.title"),
                      isDate: false,
                      isStatus: false,
                      visible: false,
                      width: "20%",
                    }];
                  const portsHeader: IHeader[] = [
                    {
                      align: "left" as DataAlignType,
                      dataField: "where",
                      header: "Host",
                      isDate: false,
                      isStatus: false,
                      width: "60%",
                      wrapped: true,
                    },
                    {
                      align: "left" as DataAlignType,
                      dataField: "specific",
                      header: translate.t("search_findings.tab_description.port", {count: 1}),
                      isDate: false,
                      isStatus: false,
                      width: "20%",
                      wrapped: true,
                    },
                    {
                      align: "left" as DataAlignType,
                      dataField: "treatment",
                      header: translate.t("search_findings.tab_description.treatment.title"),
                      isDate: false,
                      isStatus: false,
                      visible: false,
                      width: "20%",
                    }];

                  let formattedDataLines: IVulnsAttr["finding"]["linesVulns"] = dataLines;
                  let formattedDataPorts: IVulnsAttr["finding"]["portsVulns"] = dataPorts;
                  let formattedDataInputs: IVulnsAttr["finding"]["inputsVulns"] = dataInputs;
                  const formattedDataPendingVulns: IVulnsAttr["finding"]["pendingVulns"] = dataPendingVulns;

                  if (props.editMode && _.isEmpty(data.finding.releaseDate)) {
                    inputsHeader.push({
                                align: "center" as DataAlignType,
                                dataField: "id",
                                deleteFunction: handleDeleteVulnerability,
                                header: translate.t("search_findings.tab_description.action"),
                                isDate: false,
                                isStatus: false,
                                width: "10%",
                              });
                    linesHeader.push({
                                align: "center" as DataAlignType,
                                dataField: "id",
                                deleteFunction: handleDeleteVulnerability,
                                header: translate.t("search_findings.tab_description.action"),
                                isDate: false,
                                isStatus: false,
                                width: "10%",
                              });
                    portsHeader.push({
                                align: "center" as DataAlignType,
                                dataField: "id",
                                deleteFunction: handleDeleteVulnerability,
                                header: translate.t("search_findings.tab_description.action"),
                                isDate: false,
                                isStatus: false,
                                width: "10%",
                              });
                  } else if (getAnalyst) {
                    inputsHeader.push({
                      align: "left" as DataAlignType,
                      dataField: "lastAnalyst",
                      header: translate.t("search_findings.tab_description.analyst"),
                      isDate: false,
                      isStatus: false,
                      width: "30%",
                    });
                    linesHeader.push({
                      align: "left" as DataAlignType,
                      dataField: "lastAnalyst",
                      header: translate.t("search_findings.tab_description.analyst"),
                      isDate: false,
                      isStatus: false,
                      width: "30%",
                    });
                    portsHeader.push({
                      align: "left" as DataAlignType,
                      dataField: "lastAnalyst",
                      header: translate.t("search_findings.tab_description.analyst"),
                      isDate: false,
                      isStatus: false,
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
                              Organization: (window as Window & { userOrganization: string }).userOrganization,
                              User: (window as Window & { userName: string }).userName,
                            });
                          msgSuccess(
                            translate.t("search_findings.tab_description.update_vulnerabilities"),
                            translate.t("proj_alerts.title_success"));
                          handleCloseTableSetClick();
                        }
                      }
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
                    selectedRows.map((selectQry: NodeListOf<Element>) => {
                      selectedRowArray.push(getAttrVulnUpdate(selectQry));
                    });
                    const vulns: IVunlDataType[] = getVulnInfo(selectedRowArray, arrayVulnCategory);
                    vulns.map((vuln: IVunlDataType) => {
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
                    <React.StrictMode>
                      { dataInputs.length > 0
                        ? <React.Fragment>
                            <label className={style.vuln_title}>
                              {translate.t("search_findings.tab_description.inputs")}
                            </label>
                            <SimpleTable
                              id="inputsVulns"
                              dataset={formattedDataInputs}
                              exportCsv={false}
                              headers={inputsHeader}
                              onClickRow={(): void => undefined}
                              pageSize={10}
                              search={false}
                              enableRowSelection={
                                ((isEditable ? true : false) && _.includes([], props.userRole))
                              }
                              title=""
                              selectionMode="checkbox"
                            />
                            <br/>
                          </React.Fragment>
                        : undefined
                      }
                      { dataLines.length > 0
                        ? <React.Fragment>
                            <label className={style.vuln_title}>
                              {translate.t("search_findings.tab_description.line", {count: 2})}
                            </label>
                            <SimpleTable
                              id="linesVulns"
                              dataset={formattedDataLines}
                              exportCsv={false}
                              headers={linesHeader}
                              onClickRow={(): void => undefined}
                              pageSize={10}
                              search={false}
                              enableRowSelection={
                                ((isEditable ? true : false) && _.includes([], props.userRole))
                              }
                              title=""
                              selectionMode="checkbox"
                            />
                            <br/>
                          </React.Fragment>
                        : undefined
                      }
                      { dataPorts.length > 0
                        ? <React.Fragment>
                            <label className={style.vuln_title}>
                              {translate.t("search_findings.tab_description.port", {count: 2})}
                            </label>
                            <SimpleTable
                              id="portsVulns"
                              dataset={formattedDataPorts}
                              exportCsv={false}
                              headers={portsHeader}
                              onClickRow={(): void => undefined}
                              pageSize={10}
                              search={false}
                              enableRowSelection={
                                ((isEditable ? true : false) && _.includes([], props.userRole))
                              }
                              title=""
                              selectionMode="checkbox"
                            />
                            <br/>
                          </React.Fragment>
                        : undefined
                      }

                      <Mutation mutation={APPROVE_VULN_MUTATION} onCompleted={handleMtPendingVulnRes}>
                      { (approveVulnerability: MutationFn<IDeleteVulnAttr, {
                        approvalStatus: boolean; findingId: string; uuid: string; }>,
                         mutationResult: MutationResult): React.ReactNode => {
                        if (mutationRes.loading) {
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

                        const pendingsHeader: IHeader[] = [
                          {
                            align: "left" as DataAlignType,
                            dataField: "where",
                            header: "Where",
                            isDate: false,
                            isStatus: false,
                            width: "50%",
                            wrapped: true,
                          },
                          {
                            align: "left" as DataAlignType,
                            dataField: "specific",
                            header: translate.t("search_findings.tab_description.field"),
                            isDate: false,
                            isStatus: false,
                            width: "15%",
                            wrapped: true,
                          },
                          {
                            align: "left" as DataAlignType,
                            dataField: "currentState",
                            header: translate.t("search_findings.tab_description.state"),
                            isDate: false,
                            isStatus: true,
                            width: "15%",
                            wrapped: true,
                          },
                          {
                            align: "left" as DataAlignType,
                            dataField: "isNew",
                            header: translate.t("search_findings.tab_description.is_new"),
                            isDate: false,
                            isStatus: false,
                            width: "12%",
                            wrapped: true,
                          }];
                        if (getAnalyst) {
                          pendingsHeader.push({
                            align: "left" as DataAlignType,
                            dataField: "analyst",
                            header: translate.t("search_findings.tab_description.analyst"),
                            isDate: false,
                            isStatus: false,
                            width: "38%",
                          });
                        }
                        if (_.isEqual(props.editModePending, true)) {
                          pendingsHeader.push({
                            align: "center" as DataAlignType,
                            approveFunction: handleApproveVulnerability,
                            dataField: "id",
                            header: translate.t("search_findings.tab_description.approve"),
                            isDate: false,
                            isStatus: false,
                            width: "12%",
                          });
                          pendingsHeader.push({
                            align: "center" as DataAlignType,
                            dataField: "id",
                            deleteFunction: handleRejectVulnerability,
                            header: translate.t("search_findings.tab_description.delete"),
                            isDate: false,
                            isStatus: false,
                            width: "12%",
                          });
                          }

                        return (
                          <React.StrictMode>
                            { dataPendingVulns.length > 0 ?
                            <React.Fragment>
                              <SimpleTable
                                id="pendingVulns"
                                dataset={formattedDataPendingVulns}
                                exportCsv={false}
                                headers={pendingsHeader}
                                onClickRow={(): void => undefined}
                                pageSize={10}
                                search={false}
                                enableRowSelection={false}
                                title=""
                                selectionMode="checkbox"
                              />
                              <br/>
                            </React.Fragment>
                            : undefined
                            }
                            </React.StrictMode>
                            );
                          }}
                      </Mutation>

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

                            return (
                              <Modal
                                open={modalHidden}
                                footer={undefined}
                                headerTitle={translate.t("search_findings.tab_description.editVuln")}
                              >
                              <GenericForm
                                name="editTreatmentVulnerability"
                                onSubmit={(values: IDescriptionViewProps["dataset"]): void => {
                                  handleUpdateTreatmentVuln(values);
                                }}
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
                                      onClick={(): void => {
                                      store.dispatch(submit("editTreatmentVulnerability")); }}
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
