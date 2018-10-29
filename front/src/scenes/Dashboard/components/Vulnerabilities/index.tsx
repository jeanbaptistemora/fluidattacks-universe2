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
import { AxiosResponse } from "axios";
import _ from "lodash";
import PropTypes from "prop-types";
import React, { ComponentType } from "react";
import { DataAlignType } from "react-bootstrap-table";
import {
  InferableComponentEnhancer,
  lifecycle,
} from "recompose";
import { Reducer } from "redux";
import { StateType } from "typesafe-actions";
import { IHeader } from "../../../../components/DataTable/index";
import store from "../../../../store/index";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import reduxWrapper from "../../../../utils/reduxWrapper";
import rollbar from "../../../../utils/rollbar";
import Xhr from "../../../../utils/xhr";
import * as actions from "../../actions";
import { default as SimpleTable } from "../SimpleTable/index";
import style from "./index.css";

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
  translations: { [key: string]: string };
}

const mapStateToProps: ((arg1: StateType<Reducer>) => IVulnerabilitiesViewProps) =
  (state: StateType<Reducer>): IVulnerabilitiesViewProps => ({
    ...state,
    dataInputs: state.dashboard.vulnerabilities.dataInputs,
    dataLines: state.dashboard.vulnerabilities.dataLines,
    dataPorts: state.dashboard.vulnerabilities.dataPorts,
  });

const enhance: InferableComponentEnhancer<{}> =
lifecycle({
  componentDidMount(): void {
    store.dispatch(actions.clearResources());
    const { findingId, translations }: any = this.props;
    let gQry: string;
    gQry = `{
      finding(identifier: "${findingId}") {
        id
        access
        success
        errorMessage
        portsVulns: vulnerabilities(
          vulnType: "ports", state: "open") {
          ...vulnInfo
        }
        linesVulns: vulnerabilities(
          vulnType: "lines", state: "open") {
          ...vulnInfo
        }
        inputsVulns: vulnerabilities(
          vulnType: "inputs", state: "open") {
          ...vulnInfo
        }
      }
    }
    fragment vulnInfo on Vulnerability {
      vulnType
      where
      specific
      currentState
      id
      findingId
    }`;
    new Xhr().request(gQry, "An error occurred getting vulnerabilities")
    .then((resp: AxiosResponse) => {
      if (!resp.data.error) {
        if (resp.data.data.finding !== undefined && resp.data.data.finding.access) {
          if (resp.data.data.finding.success) {
            store.dispatch(actions.loadVulnerabilities(
              resp.data.data.finding.inputsVulns,
              resp.data.data.finding.linesVulns,
              resp.data.data.finding.portsVulns,
            ));
          } else if (resp.data.data.finding.errorMessage === "Error in file") {
            msgError(translations["search_findings.tab_description.errorVuln"]);
          }
        } else {
          msgError(translations["proj_alerts.access_denied"]);
        }
      } else {
        msgError(translations["proj_alerts.error_textsad"]);
      }
    })
    .catch((error: string) => {
      msgError(translations["proj_alerts.error_textsad"]);
      rollbar.error(error);
    });
  },
});

const deleteVulnerability: ((vulnInfo: { [key: string]: string } | undefined) => void) =
  (vulnInfo: { [key: string]: string } | undefined): void => {
    if (vulnInfo !== undefined) {
      let gQry: string;
      gQry = `mutation {
        deleteVulnerability(id: "${vulnInfo.id}", findingId: "${vulnInfo.findingId}"){
          access,
          success
        }
      }`;
      new Xhr().request(gQry, "An error occurred getting vulnerabilities")
      .then((resp: AxiosResponse) => {
        if (!resp.data.error) {
          if (resp.data.data.deleteVulnerability !== undefined && resp.data.data.deleteVulnerability.access) {
            if (resp.data.data.deleteVulnerability.success) {
              msgSuccess("Vulnerabilitiy was deleted of this finding", "Congratulations");
              location.reload();
            } else {
              msgError("There is an error :(");
            }
          } else {
            msgError("Access denied or project not found");
          }
        } else {
          msgError("There is an error :(");
        }
      })
      .catch((error: string) => {
        msgError("There is an error :(");
        rollbar.error(error);
      });
    }
};

const getSpecific: ((line: { [key: string]: string }) => number) =
  (line: { [key: string]: string }): number =>
    parseInt(line.specific, 10);

const compareNumbers: ((a: number, b: number) => number) =
  (a: number, b: number): number =>
    a - b;

const groupSpecific: ((lines: IVulnerabilitiesViewProps["dataLines"]) => IVulnerabilitiesViewProps["dataLines"]) =
  (lines: IVulnerabilitiesViewProps["dataLines"]): IVulnerabilitiesViewProps["dataLines"] => {
    const groups: { [key: string]: IVulnerabilitiesViewProps["dataLines"] }  = _.groupBy(lines, "where");
    const specificGrouped: IVulnerabilitiesViewProps["dataLines"] =
    _.map(groups, (line: IVulnerabilitiesViewProps["dataLines"]) =>
      ({
          currentState: line[0].currentState,
          specific: line.map(getSpecific)
                  .sort(compareNumbers)
                  .toString(),
          vulnType: line[0].vulnType,
          where: line[0].where,
      }));

    return specificGrouped;
};

export const vulnsViewComponent: React.SFC<IVulnerabilitiesViewProps> =
  (props: IVulnerabilitiesViewProps): JSX.Element => {
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
      header: props.translations["search_findings.tab_description.field"],
      isDate: false,
      isStatus: false,
      width: "30%",
    }];
  const linesHeader: IHeader[] = [
    {
      align: "left" as DataAlignType,
      dataField: "where",
      header: props.translations["search_findings.tab_description.path"],
      isDate: false,
      isStatus: false,
      width: "70%",
    },
    {
      align: "left" as DataAlignType,
      dataField: "specific",
      header: props.translations["search_findings.tab_description.line"],
      isDate: false,
      isStatus: false,
      width: "30%",
    }];
  const portsHeader: IHeader[] = [
    {
      align: "left" as DataAlignType,
      dataField: "where",
      header: props.translations["search_findings.tab_description.port"],
      isDate: false,
      isStatus: false,
      width: "70%",
    },
    {
      align: "left" as DataAlignType,
      dataField: "specific",
      header: "IP",
      isDate: false,
      isStatus: false,
      width: "30%",
    }];
  let dataLines: IVulnerabilitiesViewProps["dataLines"] = props.dataLines;
  if (props.editMode) {
    inputsHeader.push({
                align: "center" as DataAlignType,
                dataField: "id",
                deleteFunction: deleteVulnerability,
                header: props.translations["search_findings.tab_description.action"],
                isDate: false,
                isStatus: false,
                width: "10%",
              });
    linesHeader.push({
                align: "center" as DataAlignType,
                dataField: "id",
                deleteFunction: deleteVulnerability,
                header: props.translations["search_findings.tab_description.action"],
                isDate: false,
                isStatus: false,
                width: "10%",
              });
    portsHeader.push({
                align: "center" as DataAlignType,
                dataField: "id",
                deleteFunction: deleteVulnerability,
                header: props.translations["search_findings.tab_description.action"],
                isDate: false,
                isStatus: false,
                width: "10%",
              });
  } else {
    dataLines = groupSpecific(props.dataLines);
  }

  return (
    <React.StrictMode>
    { props.dataInputs.length > 0
      ? <React.Fragment>
          <label className={style.vuln_title}>{props.translations["search_findings.tab_description.inputs"]}</label>
          <SimpleTable
            id="inputsVulns"
            dataset={props.dataInputs}
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
    { props.dataLines.length > 0
      ? <React.Fragment>
          <label className={style.vuln_title}>{props.translations["search_findings.tab_description.lines"]}</label>
          <SimpleTable
            id="linesVulns"
            dataset={dataLines}
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
    { props.dataPorts.length > 0
      ? <React.Fragment>
          <label className={style.vuln_title}>{props.translations["search_findings.tab_description.ports"]}</label>
          <SimpleTable
            id="portsVulns"
            dataset={props.dataPorts}
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
  </React.StrictMode>
  );
};

/**
 *  File Input's propTypes Definition
 */
vulnsViewComponent.propTypes = {
  dataInputs: PropTypes.array,
  dataLines: PropTypes.array,
  dataPorts: PropTypes.array,
  editMode: PropTypes.bool,
  findingId: PropTypes.string,
  translations: PropTypes.object,
};

vulnsViewComponent.defaultProps = {
  editMode: false,
  findingId: "",
  translations: {},
};

export const vulnsView: ComponentType<IVulnerabilitiesViewProps> = reduxWrapper
(
  enhance(vulnsViewComponent) as React.StatelessComponent<IVulnerabilitiesViewProps>,
  mapStateToProps,
);
