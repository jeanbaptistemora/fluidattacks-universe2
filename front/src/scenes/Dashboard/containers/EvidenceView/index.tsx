/* tslint:disable jsx-no-multiline-js jsx-no-lambda
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that dynamically renders the images
 * JSX-NO-LAMBDA: Disabling this rule is necessary for the sake of simplicity and
 * readability of the code that binds click events
 */

import _ from "lodash";
import React from "react";
import { Row } from "react-bootstrap";
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
import { evidenceImage as EvidenceImage } from "../../components/EvidenceImage/index";
import * as actions from "./actions";

export interface IEvidenceViewProps {
  currentIndex: number;
  images: Array<{ description: string; url: string }>;
  isEditing: boolean;
  isImageOpen: boolean;
}

const renderImages: ((props: IEvidenceViewProps) => JSX.Element) =
  (props: IEvidenceViewProps): JSX.Element => {
    let findingBaseUrl: string;
    findingBaseUrl = `${window.location.href.split("dashboard#!/")[0]}${window.location.href.split("dashboard#!/")[1]}`;
    let emptyImage: string;
    emptyImage = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=";

    return (
      <div>
        {props.images.map((image: IEvidenceViewProps["images"][0], index: number) =>
          props.isEditing || !_.isEmpty(image.url) ?
            <EvidenceImage
              key={index}
              name={`evidence${index}`}
              description={image.description}
              isDescriptionEditable={index > 1}
              isEditing={props.isEditing}
              url={_.isEmpty(image.url) ? `data:image/png;base64,${emptyImage}` : `${findingBaseUrl}/${image.url}`}
              onClick={
                props.isEditing
                  ? (): void => undefined
                  : (): void => { store.dispatch(actions.openEvidence(index)); }
              }
              onUpdate={(): void => undefined}
            />
            : <div />)}
      </div>
    );
  };

const renderLightBox: ((props: IEvidenceViewProps) => JSX.Element) = (props: IEvidenceViewProps): JSX.Element => {
  let findingBaseUrl: string; findingBaseUrl =
    `${window.location.href.split("dashboard#!/")[0]}${window.location.href.split("dashboard#!/")[1]}`;
  const evidenceImages: IEvidenceViewProps["images"] =
    props.images.filter((image: IEvidenceViewProps["images"][0]) => !_.isEmpty(image.url));
  const nextIndex: number = (props.currentIndex + 1) % evidenceImages.length;
  const previousIndex: number = (props.currentIndex + evidenceImages.length - 1) % evidenceImages.length;

  return (
    <Lightbox
      imageTitle={evidenceImages[props.currentIndex].description}
      imagePadding={50}
      mainSrc={`${findingBaseUrl}/${evidenceImages[props.currentIndex].url}`}
      nextSrc={`${findingBaseUrl}/${evidenceImages[nextIndex].url}`}
      prevSrc={`${findingBaseUrl}/${evidenceImages[previousIndex].url}`}
      onCloseRequest={(): void => { store.dispatch(actions.closeEvidence()); }}
      onMovePrevRequest={(): void => {
        store.dispatch(actions.moveEvidenceIndex(props.currentIndex, evidenceImages.length, "previous"));
      }}
      onMoveNextRequest={(): void => {
        store.dispatch(actions.moveEvidenceIndex(props.currentIndex, evidenceImages.length, "next"));
      }}
      reactModalStyle={{ content: { top: "80px" } }}
    />
  );
};

export const component: React.SFC<IEvidenceViewProps> = (props: IEvidenceViewProps): JSX.Element => (
  <React.StrictMode>
    <Row>
      {renderImages(props)}
    </Row>
    {props.isImageOpen ? renderLightBox(props) : undefined}
  </React.StrictMode>
);

export const evidenceView: React.ComponentType<IEvidenceViewProps> = reduxWrapper(
  component,
  (state: StateType<Reducer>): IEvidenceViewProps => ({
    ...state.dashboard.evidence,
  }),
);
