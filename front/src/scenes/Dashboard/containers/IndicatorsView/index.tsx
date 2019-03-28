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
import { Col, Glyphicon, Row } from "react-bootstrap";
import {
  InferableComponentEnhancer,
  lifecycle,
} from "recompose";
import { AnyAction, Reducer } from "redux";
import { ThunkDispatch } from "redux-thunk";
import { StateType } from "typesafe-actions";
import { Button } from "../../../../components/Button/index";
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
  deletionDate: string;
  projectName: string;
  subscription: string;
  tagsDataset: string[];
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

const removeTag: ((arg1: string) => void) = (projectName: string): void => {
  const selectedQry: NodeListOf<Element> = document.querySelectorAll("#tblTags tr input:checked");
  if (selectedQry.length > 0) {
    if (selectedQry[0].closest("tr") !== null) {
      const selectedRow: Element = selectedQry[0].closest("tr") as Element;
      const tag: string | null = selectedRow.children[1].textContent;
      const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
        store.dispatch as ThunkDispatch<{}, {}, AnyAction>
      );

      thunkDispatch(actions.removeTag(projectName, tag));
    } else {
      msgError(translate.t("proj_alerts.error_textsad"));
      rollbar.error("An error occurred removing tags");
    }
  } else {
    msgError(translate.t("search_findings.tab_resources.no_selection"));
  }
};

const saveTags: (
  (tags: IIndicatorsViewProps["tagsDataset"], projectName: IIndicatorsViewProps["projectName"],
   currentEnvs: IIndicatorsViewProps["tagsDataset"],
  ) => void) =
  (tags: IIndicatorsViewProps["tagsDataset"], projectName: IIndicatorsViewProps["projectName"],
   currentEnvs: IIndicatorsViewProps["tagsDataset"],
  ): void => {
    let containsRepeated: boolean;
    containsRepeated = tags.filter(
      (newItem: IIndicatorsViewProps["tagsDataset"][0]) => _.findIndex(
        currentEnvs,
        (currentItem: IIndicatorsViewProps["tagsDataset"][0]) =>
          currentItem === newItem,
      ) > -1).length > 0;
    if (containsRepeated) {
      msgError(translate.t("search_findings.tab_resources.repeated_item"));
    } else {
      const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
        store.dispatch as ThunkDispatch<{}, {}, AnyAction>
      );
      thunkDispatch(actions.saveTags(projectName, tags));
    }
  };

const mapStateToProps: ((arg1: StateType<Reducer>) => IIndicatorsViewProps) =
  (state: StateType<Reducer>): IIndicatorsViewProps => ({
    ...state,
    addModal: state.dashboard.indicators.addModal,
    deletionDate: state.dashboard.indicators.deletionDate,
    subscription: state.dashboard.indicators.subscription,
    tagsDataset: state.dashboard.indicators.tags,
  });

const renderTagsView: ((props: IIndicatorsViewProps) => JSX.Element | undefined) =
  (props: IIndicatorsViewProps): JSX.Element | undefined =>
   !_.isEmpty(props.subscription) && _.isEmpty(props.deletionDate) ?  (
    <React.Fragment>
      <Row>
        <Col md={12} sm={12} xs={12}>
          <Row>
            <Col md={12} sm={12} xs={12}>
              <Row>
                <Col md={12}>
                  <Col mdOffset={4} md={2} sm={6}>
                    <Button
                      id="addTag"
                      block={true}
                      bsStyle="primary"
                      onClick={(): void => { store.dispatch(actions.openAddModal()); }}
                    >
                      <Glyphicon glyph="plus"/>&nbsp;
                      {translate.t("search_findings.tab_resources.add_repository")}
                    </Button>
                  </Col>
                  <Col md={2} sm={6}>
                    <Button
                      id="removeTag"
                      block={true}
                      bsStyle="primary"
                      onClick={(): void => { removeTag(props.projectName); }}
                    >
                      <Glyphicon glyph="minus"/>&nbsp;
                      {translate.t("search_findings.tab_resources.remove_repository")}
                    </Button>
                  </Col>
                </Col>
              </Row>
              <Row>
                <Col md={12} sm={12}>
                  <DataTable
                    dataset={props.tagsDataset.map((tagName: string) => ({tagName}))}
                    onClickRow={(): void => {}}
                    enableRowSelection={true}
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
      <AddTagsModal
        isOpen={props.addModal.open}
        onClose={(): void => { store.dispatch(actions.closeAddModal()); }}
        onSubmit={(values: { tags: IIndicatorsViewProps["tagsDataset"] }): void => {
          saveTags(values.tags, props.projectName, props.tagsDataset);
        }}
      />
    </React.Fragment>
    ) : undefined;

export const component: React.SFC<IIndicatorsViewProps> = (props: IIndicatorsViewProps): JSX.Element => {
  const userEmail: string = (window as Window & { userEmail: string }).userEmail;

  return (
    <React.StrictMode>
      { _.endsWith(userEmail, "@fluidattacks.com") || _.endsWith(userEmail, "@bancolombia.com.co")
        ? renderTagsView(props)
        : undefined
      }
    </React.StrictMode>
  );
};

export const indicatorsView: ComponentType<IIndicatorsViewProps> = reduxWrapper
(
  enhance(component) as React.StatelessComponent<IIndicatorsViewProps>,
  mapStateToProps,
);
