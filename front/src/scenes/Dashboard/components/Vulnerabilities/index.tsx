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
import React from "react";
import { Mutation, MutationFn, MutationResult, Query, QueryResult } from "react-apollo";
import { Col, Row } from "react-bootstrap";
import { DataAlignType } from "react-bootstrap-table";
import { AnyAction } from "redux";
import { ThunkDispatch } from "redux-thunk";
import { Button } from "../../../../components/Button/index";
import { IHeader } from "../../../../components/DataTable/index";
import { FluidIcon } from "../../../../components/FluidIcon";
import store from "../../../../store/index";
import { hidePreloader, showPreloader } from "../../../../utils/apollo";
import { handleGraphQLErrors } from "../../../../utils/formatHelpers";
import { msgSuccess } from "../../../../utils/notifications";
import translate from "../../../../utils/translations/translate";
import { isValidVulnsFile } from "../../../../utils/validations";
import * as actions from "../../actions";
import { fileInput as FileInput } from "../../components/FileInput/index";
import { default as SimpleTable } from "../SimpleTable/index";
import style from "./index.css";
import { DELETE_VULN_MUTATION, GET_VULNERABILITIES } from "./queries";
import { IDeleteVulnAttr, IVulnsAttr } from "./types";

export interface IVulnerabilitiesViewProps {
  dataInputs: Array<{
    currentState: string; specific: string;
    vulnType: string; where: string;
  }>;
  dataLines: Array<{
    currentState: string; specific: string;
    vulnType: string; where: string;
  }>;
  dataPorts: Array<{
    currentState: string; specific: string;
    vulnType: string; where: string;
  }>;
  editMode: boolean;
  findingId: string;
  releaseDate: string;
  state: string;
  userRole: string;
}

type IVulnType = (IVulnerabilitiesViewProps["dataLines"] | IVulnerabilitiesViewProps["dataPorts"] |
  IVulnerabilitiesViewProps["dataPorts"]);

const filterState:
  ((dataVuln: IVulnerabilitiesViewProps["dataInputs"], state: string) => IVulnerabilitiesViewProps["dataInputs"]) =
    (dataVuln: IVulnerabilitiesViewProps["dataInputs"], state: string): IVulnerabilitiesViewProps["dataInputs"] =>

      dataVuln.filter((vuln: IVulnerabilitiesViewProps["dataInputs"][0]) => vuln.currentState === state);

const specificToNumber: ((line: { [key: string]: string }) => number) =
  (line: { [key: string]: string }): number =>
    parseInt(line.specific, 10);

const getSpecific: ((line: { [key: string]: string }) => string) =
  (line: { [key: string]: string }): string =>
    line.specific;

const compareNumbers: ((a: number, b: number) => number) =
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

  return ranges.toString();
};

const groupValues: ((values: number[]) => string) =
  (values: number[]): string =>
    getRanges(values.sort(compareNumbers));

const groupSpecific: ((lines: IVulnType) => IVulnType) = (lines: IVulnType): IVulnType => {
  const groups: { [key: string]: IVulnType }  = _.groupBy(lines, "where");
  const specificGrouped: IVulnType =
  _.map(groups, (line: IVulnType) =>
    ({
        currentState: line[0].currentState,
        specific: line[0].vulnType === "inputs" ? line.map(getSpecific)
          .toString() : groupValues(line.map(specificToNumber)),
        vulnType: line[0].vulnType,
        where: line[0].where,
    }));

  return specificGrouped;
};

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
            <FileInput fileName="" icon="search" id="vulnerabilities" type=".yaml, .yml" visible={true} />
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

export const vulnsViewComponent: React.FC<IVulnerabilitiesViewProps> =
  (props: IVulnerabilitiesViewProps): JSX.Element =>

  (
    <Query query={GET_VULNERABILITIES} variables={{ identifier: props.findingId }} notifyOnNetworkStatusChange={true}>
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
            const dataInputs: IVulnsAttr["finding"]["inputsVulns"] = filterState(data.finding.inputsVulns, props.state);
            const dataLines: IVulnsAttr["finding"]["linesVulns"] = filterState(data.finding.linesVulns, props.state);
            const dataPorts: IVulnsAttr["finding"]["portsVulns"] = filterState(data.finding.portsVulns, props.state);

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
                      width: "70%",
                    },
                    {
                      align: "left" as DataAlignType,
                      dataField: "specific",
                      header: translate.t("search_findings.tab_description.field"),
                      isDate: false,
                      isStatus: false,
                      width: "30%",
                    }];
                  const linesHeader: IHeader[] = [
                    {
                      align: "left" as DataAlignType,
                      dataField: "where",
                      header: translate.t("search_findings.tab_description.path"),
                      isDate: false,
                      isStatus: false,
                      width: "70%",
                    },
                    {
                      align: "left" as DataAlignType,
                      dataField: "specific",
                      header: translate.t("search_findings.tab_description.line", {count: 1}),
                      isDate: false,
                      isStatus: false,
                      width: "30%",
                    }];
                  const portsHeader: IHeader[] = [
                    {
                      align: "left" as DataAlignType,
                      dataField: "where",
                      header: "Host",
                      isDate: false,
                      isStatus: false,
                      width: "70%",
                    },
                    {
                      align: "left" as DataAlignType,
                      dataField: "specific",
                      header: translate.t("search_findings.tab_description.port", {count: 1}),
                      isDate: false,
                      isStatus: false,
                      width: "30%",
                    }];

                  let formattedDataLines: IVulnsAttr["finding"]["linesVulns"] = dataLines;
                  let formattedDataPorts: IVulnsAttr["finding"]["portsVulns"] = dataPorts;
                  let formattedDataInputs: IVulnsAttr["finding"]["inputsVulns"] = dataInputs;

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
                  } else {
                    formattedDataLines = groupSpecific(dataLines);
                    formattedDataPorts = groupSpecific(dataPorts);
                    formattedDataInputs = groupSpecific(dataInputs);
                  }

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
                              enableRowSelection={false}
                              title=""
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
                              enableRowSelection={false}
                              title=""
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
                              enableRowSelection={false}
                              title=""
                            />
                            <br/>
                          </React.Fragment>
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

export { vulnsViewComponent as VulnerabilitiesView };
