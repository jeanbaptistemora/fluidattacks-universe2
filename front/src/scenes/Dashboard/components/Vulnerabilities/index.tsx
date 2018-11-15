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
import _ from "lodash";
import React, { ComponentType } from "react";
import { DataAlignType } from "react-bootstrap-table";
import {
  InferableComponentEnhancer,
  lifecycle,
} from "recompose";
import { AnyAction, Reducer } from "redux";
import { ThunkDispatch } from "redux-thunk";
import { StateType } from "typesafe-actions";
import { IHeader } from "../../../../components/DataTable/index";
import store from "../../../../store/index";
import reduxWrapper from "../../../../utils/reduxWrapper";
import translate from "../../../../utils/translations/translate";
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
  state: string;
}

const filterState:
  ((dataVuln: IVulnerabilitiesViewProps["dataInputs"], state: string) => IVulnerabilitiesViewProps["dataInputs"]) =
    (dataVuln: IVulnerabilitiesViewProps["dataInputs"], state: string): IVulnerabilitiesViewProps["dataInputs"] =>

      dataVuln.filter((vuln: IVulnerabilitiesViewProps["dataInputs"][0]) => vuln.currentState === state);

const mapStateToProps: ((arg1: StateType<Reducer>, arg2: IVulnerabilitiesViewProps) => IVulnerabilitiesViewProps) =
  (state: StateType<Reducer>, ownProps: IVulnerabilitiesViewProps): IVulnerabilitiesViewProps => {
    const stateValue: IVulnerabilitiesViewProps = state.dashboard.vulnerabilities;
    const dataInputs: IVulnerabilitiesViewProps["dataInputs"] = filterState(stateValue.dataInputs, ownProps.state);
    const dataLines: IVulnerabilitiesViewProps["dataLines"] = filterState(stateValue.dataLines, ownProps.state);
    const dataPorts: IVulnerabilitiesViewProps["dataPorts"] = filterState(stateValue.dataPorts, ownProps.state);

    return ({
      ...state,
      dataInputs,
      dataLines,
      dataPorts,
    });
  };

const enhance: InferableComponentEnhancer<{}> =
lifecycle({
  componentDidMount(): void {
    store.dispatch(actions.clearResources());
    const { findingId } = this.props as IVulnerabilitiesViewProps;
    const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, {}, AnyAction>
    );

    thunkDispatch(actions.loadVulnerabilities(findingId));
  },
});

const deleteVulnerability: ((vulnInfo: { [key: string]: string } | undefined) => void) =
  (vulnInfo: { [key: string]: string } | undefined): void => {
    if (vulnInfo !== undefined) {
      const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
        store.dispatch as ThunkDispatch<{}, {}, AnyAction>
      );

      thunkDispatch(actions.deleteVulnerability(vulnInfo));
    }
};

const getSpecific: ((line: { [key: string]: string }) => number) =
  (line: { [key: string]: string }): number =>
    parseInt(line.specific, 10);

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

const groupSpecific: ((lines: IVulnerabilitiesViewProps["dataLines"]) => IVulnerabilitiesViewProps["dataLines"]) =
  (lines: IVulnerabilitiesViewProps["dataLines"]): IVulnerabilitiesViewProps["dataLines"] => {
    const groups: { [key: string]: IVulnerabilitiesViewProps["dataLines"] }  = _.groupBy(lines, "where");
    const specificGrouped: IVulnerabilitiesViewProps["dataLines"] =
    _.map(groups, (line: IVulnerabilitiesViewProps["dataLines"]) =>
      ({
          currentState: line[0].currentState,
          specific: groupValues(line.map(getSpecific)),
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
  let dataLines: IVulnerabilitiesViewProps["dataLines"] = props.dataLines;
  if (props.editMode) {
    inputsHeader.push({
                align: "center" as DataAlignType,
                dataField: "id",
                deleteFunction: deleteVulnerability,
                header: translate.t("search_findings.tab_description.action"),
                isDate: false,
                isStatus: false,
                width: "10%",
              });
    linesHeader.push({
                align: "center" as DataAlignType,
                dataField: "id",
                deleteFunction: deleteVulnerability,
                header: translate.t("search_findings.tab_description.action"),
                isDate: false,
                isStatus: false,
                width: "10%",
              });
    portsHeader.push({
                align: "center" as DataAlignType,
                dataField: "id",
                deleteFunction: deleteVulnerability,
                header: translate.t("search_findings.tab_description.action"),
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
          <label className={style.vuln_title}>{translate.t("search_findings.tab_description.inputs")}</label>
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
          <label className={style.vuln_title}>{translate.t("search_findings.tab_description.line", {count: 2})}</label>
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
          <label className={style.vuln_title}>{translate.t("search_findings.tab_description.port", {count: 2})}</label>
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

vulnsViewComponent.defaultProps = {
  editMode: false,
  findingId: "",
  state: "",
};

export const vulnsView: ComponentType<IVulnerabilitiesViewProps> = reduxWrapper
(
  enhance(vulnsViewComponent) as React.StatelessComponent<IVulnerabilitiesViewProps>,
  mapStateToProps,
);
