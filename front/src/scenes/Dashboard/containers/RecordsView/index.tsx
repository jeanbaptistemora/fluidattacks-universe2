/* tslint:disable jsx-no-lambda
 * Disabling this rule is necessary for the sake of simplicity and
 * readability of the code that binds click events
 */

import React, { ComponentType } from "react";
import { Button, Col, Glyphicon, Row } from "react-bootstrap";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { AnyAction, Reducer } from "redux";
import { ThunkDispatch } from "redux-thunk";
import { StateType } from "typesafe-actions";
import { dataTable as DataTable } from "../../../../components/DataTable/index";
import store from "../../../../store/index";
import reduxWrapper from "../../../../utils/reduxWrapper";
import translate from "../../../../utils/translations/translate";
import { isValidEvidenceFile } from "../../../../utils/validations";
import { fileInput as FileInput } from "../../components/FileInput/index";
import * as actions from "./actions";

export interface IRecordsViewProps {
  canEdit: boolean;
  /* tslint:disable-next-line: no-any
   * Disabling here is necessary because records dataset
   * may vary between findings
   */
  dataset: any[];
  findingId: string;
  isEditing: boolean;
}

const updateRecords: ((arg1: string) => void) = (findingId: string): void => {

  if (isValidEvidenceFile("#evidence8")) {
    const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, {}, AnyAction>
    );

    thunkDispatch(actions.updateRecords(findingId));
  }
};

const renderUploadField: ((arg1: IRecordsViewProps) => JSX.Element) =
  (props: IRecordsViewProps): JSX.Element => (
  <Row>
    <Col md={4} mdOffset={6} xs={12} sm={12}>
      <div>
        <FileInput
          fileName="evidence8[]"
          icon="search"
          id="evidence8"
          type=".csv"
          visible={true}
        />
      </div>
    </Col>
      <Col sm={2}>
        <Button
          bsStyle="primary"
          block={true}
          onClick={(): void => { updateRecords(props.findingId); }}
        >
          <Glyphicon glyph="cloud-upload"/>
          &nbsp;{translate.t("search_findings.tab_evidence.update")}
        </Button>
      </Col>
  </Row>
);

const renderEditPanel: ((arg1: IRecordsViewProps) => JSX.Element) =
  (props: IRecordsViewProps): JSX.Element => (
    <React.Fragment>
      <Row>
        <Col md={2} mdOffset={10} xs={12} sm={12}>
          <Button
            bsStyle="primary"
            block={true}
            onClick={(): void => { store.dispatch(actions.editRecords()); }}
          >
            <Glyphicon glyph="edit"/>
            &nbsp;{translate.t("search_findings.tab_evidence.editable")}
          </Button>
        </Col>
      </Row>
      <br/>
      {props.isEditing ? renderUploadField(props) : undefined}
    </React.Fragment>
);

const renderTable: ((arg1: IRecordsViewProps["dataset"]) => JSX.Element) =
  (dataset: IRecordsViewProps["dataset"]): JSX.Element => (
    <DataTable
      dataset={dataset}
      onClickRow={(): void => undefined}
      enableRowSelection={false}
      exportCsv={false}
      headers={[]}
      id="tblRecords"
      pageSize={15}
      title=""
    />
);

export const component: React.SFC<IRecordsViewProps> =
  (props: IRecordsViewProps): JSX.Element => (
    <React.StrictMode>
      <Row>
        {props.canEdit ? renderEditPanel(props) : undefined}
      </Row>
      <Row>
        {renderTable(props.dataset)}
      </Row>
    </React.StrictMode>
);

const enhance: InferableComponentEnhancer<{}> =
lifecycle({
  componentDidMount(): void {
    const { findingId }: IRecordsViewProps = this.props as IRecordsViewProps;
    const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, {}, AnyAction>
    );
    thunkDispatch(actions.loadRecords(findingId));
  },
});

export const recordsView: ComponentType<IRecordsViewProps> = reduxWrapper
(
  enhance(component) as React.SFC<IRecordsViewProps>,
  (state: StateType<Reducer>): IRecordsViewProps => ({
    ...state.dashboard.records,
  }),
);
