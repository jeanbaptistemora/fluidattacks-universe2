/* eslint-disable react/forbid-component-props
  --------
  We need className to override default styles from react-bootstrap.
  */
import {
  faDownload,
  faExpandArrowsAlt,
  faHourglassHalf,
  faInfoCircle,
  faSyncAlt,
  faTimes,
  faWrench,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { ComponentSize } from "@rehooks/component-size";
import useComponentSize from "@rehooks/component-size";
import _ from "lodash";
import { track as mixpanelTrack } from "mixpanel-browser";
import React, {
  useCallback,
  useContext,
  useMemo,
  useRef,
  useState,
} from "react";

import { Modal } from "components/Modal";
import {
  allowedDocumentNames,
  allowedDocumentTypes,
  mergedDocuments,
} from "graphics/components/Graphic/ctx";
import { FilterButton } from "graphics/components/Graphic/filterButton";
import styles from "graphics/components/Graphic/index.css";
import type { IGraphicProps } from "graphics/types";
import {
  ButtonGroup,
  ButtonToolbar,
  GraphicButton,
  GraphicPanelCollapse,
  GraphicPanelCollapseBody,
  GraphicPanelCollapseFooter,
  GraphicPanelCollapseHeader,
} from "styles/styledComponents";
import type { ISecureStoreConfig } from "utils/secureStore";
import { secureStoreContext } from "utils/secureStore";
import { translate } from "utils/translations/translate";

const glyphPadding: number = 15;
const fontSize: number = 16;
const pixelsSensitivity: number = 5;
const minWidthToShowButtons: number = 320;
const bigGraphicSize: ComponentSize = {
  height: 400,
  width: 1000,
};

interface IComponentSizeProps {
  readonly height: number;
  readonly width: number;
}

interface IReadonlyGraphicProps {
  readonly documentName: string;
  readonly documentType: string;
  readonly entity: string;
  readonly generatorName: string;
  readonly generatorType: string;
  readonly subject: string;
}

function buildUrl(
  props: IReadonlyGraphicProps,
  size: IComponentSizeProps,
  subjectName: string,
  documentName: string
): string {
  const roundedHeight: number =
    pixelsSensitivity * Math.floor(size.height / pixelsSensitivity);
  const roundedWidth: number =
    pixelsSensitivity * Math.floor(size.width / pixelsSensitivity);

  const url: URL = new URL("/graphic", window.location.origin);
  url.searchParams.set("documentName", documentName);
  url.searchParams.set("documentType", props.documentType);
  url.searchParams.set("entity", props.entity);
  url.searchParams.set("generatorName", props.generatorName);
  url.searchParams.set("generatorType", props.generatorType);
  url.searchParams.set("height", roundedHeight.toString());
  url.searchParams.set("subject", subjectName);
  url.searchParams.set("width", roundedWidth.toString());

  return url.toString();
}

export const Graphic: React.FC<IGraphicProps> = (
  props: Readonly<IGraphicProps>
): JSX.Element => {
  const {
    bsHeight,
    className,
    documentName,
    documentType,
    entity,
    footer,
    infoLink,
    reportMode,
    subject,
    title,
  } = props;

  // Hooks
  const fullRef: React.MutableRefObject<HTMLDivElement | null> = useRef(null);
  const headRef: React.MutableRefObject<HTMLDivElement | null> = useRef(null);
  const bodyRef: React.MutableRefObject<HTMLIFrameElement | null> =
    useRef(null);
  const modalRef: React.MutableRefObject<HTMLIFrameElement | null> =
    useRef(null);
  const modalBodyRef: React.MutableRefObject<HTMLIFrameElement | null> =
    useRef(null);

  // More hooks
  const fullSize: ComponentSize = useComponentSize(fullRef);
  const headSize: ComponentSize = useComponentSize(headRef);
  const bodySize: ComponentSize = useComponentSize(bodyRef);
  const modalSize: ComponentSize = useComponentSize(modalBodyRef);

  const [subjectName, setSubjectName] = useState(subject);
  const [currentDocumentName, setCurrentDocumentName] = useState(documentName);
  const [expanded, setExpanded] = useState(reportMode);
  const [fullScreen, setFullScreen] = useState(false);
  const [iframeState, setIframeState] = useState("loading");

  const secureStore: ISecureStoreConfig = useContext(secureStoreContext);

  // Yet more hooks
  const iframeSrc: string = useMemo(
    (): string =>
      secureStore.retrieveBlob(
        buildUrl(
          { ...props, documentName: currentDocumentName, subject: subjectName },
          bodySize,
          subjectName,
          currentDocumentName
        )
      ),
    [bodySize, props, secureStore, subjectName, currentDocumentName]
  );
  const modalIframeSrc: string = useMemo(
    (): string =>
      secureStore.retrieveBlob(
        buildUrl(
          { ...props, documentName: currentDocumentName, subject: subjectName },
          modalSize,
          subjectName,
          currentDocumentName
        )
      ),
    [modalSize, props, secureStore, subjectName, currentDocumentName]
  );

  function panelOnMouseEnter(): void {
    setExpanded(true);
  }
  function panelOnMouseLeave(): void {
    setExpanded(reportMode);
  }
  function frameOnLoad(): void {
    setIframeState("ready");
    secureStore.storeIframeContent(bodyRef);
  }
  function frameOnFullScreen(): void {
    setFullScreen(true);
  }
  function frameOnFullScreenExit(): void {
    setFullScreen(false);
  }
  function frameOnRefresh(): void {
    if (bodyRef.current?.contentWindow !== null) {
      setIframeState("loading");
      bodyRef.current?.contentWindow.location.reload();
    }
  }
  function modalFrameOnLoad(): void {
    secureStore.storeIframeContent(modalBodyRef);
  }
  function modalFrameOnRefresh(): void {
    if (modalBodyRef.current?.contentWindow !== null) {
      modalBodyRef.current?.contentWindow.location.reload();
    }
  }
  function buildFileName(size: IComponentSizeProps): string {
    return `${subjectName}-${title}-${size.width}x${size.height}.html`;
  }
  function changeTothirtyDays(): void {
    setSubjectName(`${subject}_30`);
    frameOnRefresh();
  }
  function changeToNinety(): void {
    setSubjectName(`${subject}_90`);
    frameOnRefresh();
  }
  function changeToAll(): void {
    setSubjectName(subject);
    frameOnRefresh();
  }
  function changeToDefault(): void {
    setCurrentDocumentName(documentName);
    frameOnRefresh();
  }
  function changeToAlternative(): void {
    if (_.includes(Object.keys(mergedDocuments), documentName)) {
      setCurrentDocumentName(mergedDocuments[documentName].documentName);
      frameOnRefresh();
    }
  }
  function isDocumentAllowed(name: string, type: string): boolean {
    return (
      _.includes(allowedDocumentNames, name) &&
      _.includes(allowedDocumentTypes, type)
    );
  }
  function isDocumentMerged(name: string, type: string): boolean {
    return (
      _.includes(Object.keys(mergedDocuments), name) &&
      mergedDocuments[name].documentType === type
    );
  }
  function getAdditionalInfoLink(name: string, type: string): string {
    if (isDocumentMerged(name, type)) {
      return mergedDocuments[name].documentName === currentDocumentName
        ? mergedDocuments[name].alt.url
        : mergedDocuments[name].default.url;
    }

    return "";
  }

  if (
    iframeState === "ready" &&
    bodyRef.current !== null &&
    bodyRef.current.contentDocument !== null &&
    bodyRef.current.contentDocument.title.toLowerCase().includes("error")
  ) {
    setIframeState("error");
  }

  const glyphSize: number = Math.min(bodySize.height, bodySize.width) / 2;
  const glyphSizeTop: number =
    headSize.height + glyphPadding + glyphSize / 2 - fontSize;

  const track: () => void = useCallback((): void => {
    mixpanelTrack("DownloadGraphic", { currentDocumentName, entity });
  }, [currentDocumentName, entity]);

  return (
    <React.Fragment>
      <Modal
        headerTitle={
          <div className={"w-100"}>
            <div className={styles.titleBar}>
              {title}
              <ButtonToolbar className={"f5"}>
                <FilterButton
                  changeToAll={changeToAll}
                  changeToAlternative={changeToAlternative}
                  changeToDefault={changeToDefault}
                  changeToNinety={changeToNinety}
                  changeTothirtyDays={changeTothirtyDays}
                  currentDocumentName={currentDocumentName}
                  documentName={documentName}
                  documentNameFilter={isDocumentMerged(
                    documentName,
                    documentType
                  )}
                  subject={subject}
                  subjectName={subjectName}
                  timeFilter={isDocumentAllowed(documentName, documentType)}
                />
                {!_.isUndefined(infoLink) && (
                  <GraphicButton>
                    <a
                      className={"g-a"}
                      href={
                        infoLink +
                        getAdditionalInfoLink(documentName, documentType)
                      }
                      rel={"noopener noreferrer"}
                      target={"_blank"}
                    >
                      <FontAwesomeIcon icon={faInfoCircle} />
                    </a>
                  </GraphicButton>
                )}
                <GraphicButton>
                  <a
                    className={"g-a"}
                    download={buildFileName(modalSize)}
                    href={buildUrl(
                      props,
                      modalSize,
                      subjectName,
                      currentDocumentName
                    )}
                    onClick={track}
                    rel={"noopener noreferrer"}
                    target={"_blank"}
                  >
                    <FontAwesomeIcon icon={faDownload} />
                  </a>
                </GraphicButton>
                <GraphicButton onClick={modalFrameOnRefresh}>
                  <FontAwesomeIcon icon={faSyncAlt} />
                </GraphicButton>
                <GraphicButton onClick={frameOnFullScreenExit}>
                  <FontAwesomeIcon icon={faTimes} />
                </GraphicButton>
              </ButtonToolbar>
            </div>
          </div>
        }
        onEsc={frameOnFullScreenExit}
        open={fullScreen}
        size={"graphicModal"}
      >
        <div ref={modalRef} style={{ height: bigGraphicSize.height }}>
          <iframe
            className={styles.frame}
            frameBorder={"no"}
            onLoad={modalFrameOnLoad}
            ref={modalBodyRef}
            scrolling={"no"}
            src={modalIframeSrc}
            title={title}
          />
        </div>
        {_.isUndefined(footer) ? undefined : (
          <React.Fragment>
            <hr />
            <div>{footer}</div>
          </React.Fragment>
        )}
      </Modal>
      <div ref={fullRef}>
        <GraphicPanelCollapse
          className={className}
          onMouseEnter={panelOnMouseEnter}
          onMouseLeave={panelOnMouseLeave}
        >
          <div className={"report-title-pad"} ref={headRef}>
            <GraphicPanelCollapseHeader>
              <div className={styles.titleBar}>
                <div className={"w-100 report-title"}>
                  {title}
                  {expanded &&
                    !reportMode &&
                    fullSize.width > minWidthToShowButtons && (
                      <ButtonGroup className={"fr"}>
                        <FilterButton
                          changeToAll={changeToAll}
                          changeToAlternative={changeToAlternative}
                          changeToDefault={changeToDefault}
                          changeToNinety={changeToNinety}
                          changeTothirtyDays={changeTothirtyDays}
                          currentDocumentName={currentDocumentName}
                          documentName={documentName}
                          documentNameFilter={isDocumentMerged(
                            documentName,
                            documentType
                          )}
                          subject={subject}
                          subjectName={subjectName}
                          timeFilter={isDocumentAllowed(
                            documentName,
                            documentType
                          )}
                        />
                        {!_.isUndefined(infoLink) && (
                          <GraphicButton>
                            <a
                              className={"g-a"}
                              href={
                                infoLink +
                                getAdditionalInfoLink(
                                  documentName,
                                  documentType
                                )
                              }
                              rel={"noopener noreferrer"}
                              target={"_blank"}
                            >
                              <FontAwesomeIcon icon={faInfoCircle} />
                            </a>
                          </GraphicButton>
                        )}
                        <GraphicButton>
                          <a
                            className={"g-a"}
                            download={buildFileName(bigGraphicSize)}
                            href={buildUrl(
                              props,
                              bigGraphicSize,
                              subjectName,
                              currentDocumentName
                            )}
                            onClick={track}
                            rel={"noopener noreferrer"}
                            target={"_blank"}
                          >
                            <FontAwesomeIcon icon={faDownload} />
                          </a>
                        </GraphicButton>
                        <GraphicButton onClick={frameOnRefresh}>
                          <FontAwesomeIcon icon={faSyncAlt} />
                        </GraphicButton>
                        <GraphicButton onClick={frameOnFullScreen}>
                          <FontAwesomeIcon icon={faExpandArrowsAlt} />
                        </GraphicButton>
                      </ButtonGroup>
                    )}
                </div>
              </div>
            </GraphicPanelCollapseHeader>
            <hr className={styles.tinyLine} />
          </div>
          <GraphicPanelCollapseBody>
            <div style={{ height: bsHeight }}>
              <iframe
                className={styles.frame}
                frameBorder={"no"}
                onLoad={frameOnLoad}
                ref={bodyRef}
                scrolling={"no"}
                src={iframeSrc}
                style={{
                  /*
                   * The element must be rendered for C3 legends to work,
                   * so lets just hide it from the user
                   */
                  opacity: iframeState === "ready" ? 1 : 0,
                }}
                title={title}
              />
              {iframeState !== "ready" && (
                <div
                  className={styles.loadingComponent}
                  style={{
                    fontSize: glyphSize,
                    top: glyphSizeTop,
                  }}
                >
                  {iframeState === "loading" ? (
                    <FontAwesomeIcon icon={faHourglassHalf} />
                  ) : (
                    <React.Fragment>
                      <FontAwesomeIcon icon={faWrench} />
                      <p className={styles.emptyChart}>
                        {translate.t("analytics.emptyChart.text")}
                      </p>
                    </React.Fragment>
                  )}
                </div>
              )}
            </div>
          </GraphicPanelCollapseBody>
          {!_.isUndefined(footer) && (
            <GraphicPanelCollapseFooter>
              <div className={"report-footer"}>{footer}</div>
            </GraphicPanelCollapseFooter>
          )}
        </GraphicPanelCollapse>
      </div>
    </React.Fragment>
  );
};
