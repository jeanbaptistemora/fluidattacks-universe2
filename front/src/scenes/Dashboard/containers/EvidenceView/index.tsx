/* tslint:disable jsx-no-multiline-js jsx-no-lambda
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that dynamically renders the images
 * JSX-NO-LAMBDA: Disabling this rule is necessary for the sake of simplicity and
 * readability of the code that binds click events
 */

import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Col, Row } from "react-bootstrap";
import Lightbox from "react-image-lightbox";
/* tslint:disable-next-line:no-import-side-effect no-submodule-imports
 * Disabling this two rules is necessary for
 * allowing the import of default styles that React Image Lightbox needs
 * to display properly even if some of them are overridden later
 */
import "react-image-lightbox/style.css";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { AnyAction, Reducer } from "redux";
import { ThunkDispatch } from "redux-thunk";
import { StateType } from "typesafe-actions";
import { Button } from "../../../../components/Button/index";
import { FluidIcon } from "../../../../components/FluidIcon";
import store from "../../../../store/index";
import { msgError } from "../../../../utils/notifications";
import reduxWrapper from "../../../../utils/reduxWrapper";
import translate from "../../../../utils/translations/translate";
import { isFileSelected, isValidEvidenceFile } from "../../../../utils/validations";
import { evidenceImage as EvidenceImage } from "../../components/EvidenceImage/index";
import * as actions from "./actions";

export interface IEvidenceViewProps {
  canEdit: boolean;
  currentIndex: number;
  findingId: string;
  images: Array<{ description: string; url: string }>;
  isEditing: boolean;
  isImageOpen: boolean;
}

const enhance: InferableComponentEnhancer<{}> =
  lifecycle({
    componentWillUnmount(): void { store.dispatch(actions.clearEvidence()); },
    componentDidMount(): void {
      mixpanel.track(
        "FindingEvidence",
        {
          Organization: (window as Window & { userOrganization: string }).userOrganization,
          User: (window as Window & { userName: string }).userName,
        });

      const { findingId } = this.props as IEvidenceViewProps;
      const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
        store.dispatch as ThunkDispatch<{}, {}, AnyAction>
      );

      thunkDispatch(actions.loadEvidence(findingId));
    },
  });

const updateEvidence: ((values: {}, evidenceId: number, props: IEvidenceViewProps) => void) =
  (values: { [key: string]: string }, evidenceId: number, props: IEvidenceViewProps): void => {
    const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, {}, AnyAction>
    );
    let fileId: string; fileId = `#evidence${evidenceId}`;
    let descriptionField: string; descriptionField = `evidence${evidenceId}_description`;
    mixpanel.track(
      "UpdateEvidence",
      {
        Organization: (window as Window & { userOrganization: string }).userOrganization,
        User: (window as Window & { userName: string }).userName,
      });
    if (isFileSelected(fileId)) {
      if (isValidEvidenceFile(fileId)) {
        thunkDispatch(actions.updateEvidence(props.findingId, evidenceId, values[descriptionField], descriptionField));
      }
    } else if (_.isEmpty(props.images[evidenceId].url)) {
      msgError(translate.t("proj_alerts.no_file_selected"));
    } else {
      if (evidenceId > 1) {
        thunkDispatch(actions.updateEvidenceDescription(values[descriptionField], props.findingId, descriptionField));
      }
    }
  };

const renderEditPanel: ((props: IEvidenceViewProps) => JSX.Element) = (props: IEvidenceViewProps): JSX.Element => (
  <Row>
    <Col md={2} mdOffset={10} xs={12} sm={12}>
      <Button
        bsStyle="primary"
        block={true}
        onClick={(): void => { store.dispatch(actions.editEvidence(!props.isEditing)); }}
      >
        <FluidIcon icon="edit" /> {translate.t("search_findings.tab_severity.editable")}
      </Button>
    </Col>
  </Row>
);

const renderImages: ((props: IEvidenceViewProps) => JSX.Element) =
  (props: IEvidenceViewProps): JSX.Element => {
    let findingBaseUrl: string;
    findingBaseUrl = `${window.location.href.split("dashboard#!/")[0]}${window.location.href.split("dashboard#!/")[1]}`;
    let emptyImage: string;
    emptyImage = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=";

    return (
      <div>
        {(props.isEditing
          ? props.images
          : props.images.filter((image: IEvidenceViewProps["images"][0]) => !_.isEmpty(image.url)))
          .map((image: IEvidenceViewProps["images"][0], index: number) =>
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
              onUpdate={(values: {}): void => { updateEvidence(values, index, props); }}
            />,
        )}
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
      onAfterOpen={(): void => {
        /**
         * Hack:
         * Due to a bug in this component, we need to set an initial img scale so it doesn't look too small
         */
        setTimeout((): void => {
          const currentImg: HTMLImageElement =
            (document.getElementsByClassName("ril-image-current")[0] as HTMLImageElement);
          const lightboxContainer: HTMLElement = (document.getElementsByClassName("ril-inner")[0] as HTMLElement);
          const scaleFactor: number = (lightboxContainer.offsetWidth / currentImg.width) * 0.65;
          currentImg.style.transform = `scale(${scaleFactor})`;
        },         100);
      }}
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
      reactModalStyle={{ overlay: { zIndex: "1200" } }}
    />
  );
};

export const component: React.FC<IEvidenceViewProps> = (props: IEvidenceViewProps): JSX.Element => (
  <React.StrictMode>
    {props.canEdit ? renderEditPanel(props) : undefined}
    <Row>
      {renderImages(props)}
    </Row>
    {props.isImageOpen ? renderLightBox(props) : undefined}
  </React.StrictMode>
);

export const evidenceView: React.ComponentType<IEvidenceViewProps> = reduxWrapper(
  enhance(component) as React.FC<IEvidenceViewProps>,
  (state: StateType<Reducer>): IEvidenceViewProps => ({
    ...state.dashboard.evidence,
  }),
);
