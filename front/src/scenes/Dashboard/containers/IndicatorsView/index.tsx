/* tslint:disable:jsx-no-lambda jsx-no-multiline-js no-empty
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import _ from "lodash";
import React, { ComponentType } from "react";
import { Button, Col, Glyphicon, Row } from "react-bootstrap";
import {
  InferableComponentEnhancer,
  lifecycle,
} from "recompose";
import { AnyAction, Reducer } from "redux";
import { ThunkDispatch } from "redux-thunk";
import { StateType } from "typesafe-actions";
import { dataTable as DataTable } from "../../../../components/DataTable/index";
import store from "../../../../store/index";
import { msgError } from "../../../../utils/notifications";
import reduxWrapper from "../../../../utils/reduxWrapper";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { addTagsModal as AddTagsModal } from "../../components/AddTagsModal/index";
import * as actions from "./actions";

export interface IIndicatorsViewProps {
  addModal: {
    open: boolean;
  };
  tagsDataset: string[];
  projectName: string;
  subscription: string;
  deletionDate: string;
}

const enhance: InferableComponentEnhancer<{}> =
lifecycle({
  componentDidMount(): void {
    const { projectName } = this.props as IIndicatorsViewProps;
    const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, {}, AnyAction>
    );

    thunkDispatch(actions.loadTags(projectName));
  },
});

const mapStateToProps: ((arg1: StateType<Reducer>) => IIndicatorsViewProps) =
  (state: StateType<Reducer>): IIndicatorsViewProps => ({
    ...state,
    addModal: state.dashboard.indicators.addModal,
    deletionDate: state.dashboard.indicators.deletionDate,
    subscription: state.dashboard.indicators.subscription,
    tagsDataset: state.dashboard.indicators.tags,
  });

export const component: React.StatelessComponent<IIndicatorsViewProps> =
  (props: IIndicatorsViewProps): JSX.Element => (
  <React.StrictMode>
    { props.subscription && _.isEmpty(props.deletionDate)
      ?  <React.Fragment>
            <Row>
              <Col md={12} sm={12} xs={12}>
                <Row>
                  <Col md={12} sm={12} xs={12}>
                    <Row>
                      <Col md={12} sm={12}>
                        <DataTable
                          dataset={props.tagsDataset.map((tagName: string) => ({tagName}))}
                          onClickRow={(): void => {}}
                          enableRowSelection={false}
                          exportCsv={false}
                          search={false}
                          headers={[
                            {
                              dataField: "tagName",
                              header: "Tags",
                              isDate: false,
                              isStatus: false,
                            },
                          ]}
                          id="tblTags"
                          pageSize={15}
                          title={""}
                        />
                      </Col>
                    </Row>
                  </Col>
                </Row>
              </Col>
            </Row>
          </React.Fragment>
      : undefined
    }
  </React.StrictMode>
);

export const indicatorsView: ComponentType<IIndicatorsViewProps> = reduxWrapper
(
  enhance(component) as React.StatelessComponent<IIndicatorsViewProps>,
  mapStateToProps,
);