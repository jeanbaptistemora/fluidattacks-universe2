/* tslint:disable jsx-no-multiline-js jsx-no-lambda
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that dynamically renders the images
 * JSX-NO-LAMBDA: Disabling this rule is necessary for the sake of simplicity and
 * readability of the code that binds click events
 */

import React from "react";
import { Col, Row } from "react-bootstrap";
/**
 * Disabling here is necessary because
 * there are currently no available type
 * definitions for this component
 */
// @ts-ignore
import Lightbox from "react-image-lightbox";
/* tslint:disable-next-line:no-import-side-effect no-submodule-imports
 * Disabling this two rules is necessary for
 * allowing the import of default styles that React Image Lightbox needs
 * to display properly even if some of them are overridden later
 */
import "react-image-lightbox/style.css";
import { Reducer } from "redux";
import { StateType } from "typesafe-actions";
import store from "../../../../store/index";
import reduxWrapper from "../../../../utils/reduxWrapper";
import translate from "../../../../utils/translations/translate";
import * as actions from "./actions";

export interface IEvidenceViewProps {
  currentIndex: number;
  images: Array<{ description: string; url: string }>;
  isImageOpen: boolean;
}

export const component: React.SFC<IEvidenceViewProps> = (props: IEvidenceViewProps): JSX.Element => (
  <React.StrictMode>
    <Row>
      {props.images.map((image: IEvidenceViewProps["images"][0], index: number) => (
        <Col key={index} md={4} sm={6} xs={12}>
          <div className="panel panel-default">
            <div className="panel-body">
              <img
                src={image.url}
                style={{ maxWidth: "100%" }}
                className="integrates-image img-thumbnail img-responsive"
                width="600"
                height="600"
                onClick={(): void => { store.dispatch(actions.openEvidence(index)); }}
              />
            </div>
            <div className="panel-footer" style={{ backgroundColor: "#fff" }}>
              <Row>
                <label><b>{translate.t("search_findings.tab_evidence.detail")}</b></label>
              </Row>
              <Row>
                <p>{image.description}</p>
              </Row>
            </div>
          </div>
        </Col>
      ))}
    </Row>
    {props.isImageOpen ? (
      <Lightbox
        imagePadding={50}
        mainSrc={props.images[props.currentIndex].url}
        nextSrc={props.images[(props.currentIndex + 1) % props.images.length].url}
        prevSrc={props.images[(props.currentIndex + props.images.length - 1) % props.images.length].url}
        onCloseRequest={(): void => { store.dispatch(actions.closeEvidence()); }}
        onMovePrevRequest={(): void => {
          store.dispatch(actions.moveEvidenceIndex(props.currentIndex, props.images.length, "previous"));
        }}
        onMoveNextRequest={(): void => {
          store.dispatch(actions.moveEvidenceIndex(props.currentIndex, props.images.length, "next"));
        }}
        reactModalStyle={{ content: { top: "80px" } }}
      />
    ) : undefined}
  </React.StrictMode>
);

export const evidenceView: React.ComponentType<IEvidenceViewProps> = reduxWrapper(
  component,
  (state: StateType<Reducer>): IEvidenceViewProps => ({
    ...state.dashboard.evidence,
  }),
);
