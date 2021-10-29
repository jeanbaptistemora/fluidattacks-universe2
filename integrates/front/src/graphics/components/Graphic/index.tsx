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
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";

import { Modal } from "components/Modal";
import type { IDocumentValues } from "graphics/components/Graphic/ctx";
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

const MAX_RETRIES: number = 5;
const DELAY_BETWEEN_RETRIES_MS: number = 300;

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

  return roundedWidth.toString() === "0" && roundedHeight.toString() === "0"
    ? ""
    : url.toString();
}

// eslint-disable-next-line complexity
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

  const [modalRetries, setModalRetries] = useState(0);
  const [modalIframeState, setModalIframeState] = useState("loading");
  const [subjectName, setSubjectName] = useState(subject);
  const [currentDocumentName, setCurrentDocumentName] = useState(documentName);
  const [currentTitle, setCurrentTitle] = useState(title);
  const [expanded, setExpanded] = useState(reportMode);
  const [fullScreen, setFullScreen] = useState(false);
  const [iframeState, setIframeState] = useState("loading");
  const [retries, setRetries] = useState(0);

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
      setRetries(0);
      setIframeState("loading");
      bodyRef.current?.contentWindow.location.reload();
    }
  }
  function modalFrameOnLoad(): void {
    setModalIframeState("ready");
    secureStore.storeIframeContent(modalBodyRef);
  }
  function modalFrameOnRefresh(): void {
    if (modalBodyRef.current?.contentWindow !== null) {
      setModalIframeState("loading");
      setModalRetries(0);
      modalBodyRef.current?.contentWindow.location.reload();
    }
  }
  function buildFileName(size: IComponentSizeProps): string {
    return `${subjectName}-${currentTitle}-${size.width}x${size.height}.html`;
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
    setCurrentTitle(title);
    frameOnRefresh();
  }
  function changeToAlternative(index: number): void {
    if (_.includes(Object.keys(mergedDocuments), documentName)) {
      setCurrentDocumentName(
        mergedDocuments[documentName].alt[index].documentName
      );
      setCurrentTitle(mergedDocuments[documentName].alt[index].title);
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
  function getUrl(alternatives: IDocumentValues[]): string {
    return alternatives.reduce(
      (url: string, alternative: IDocumentValues): string =>
        alternative.documentName === currentDocumentName
          ? alternative.url
          : url,
      ""
    );
  }
  function getAdditionalInfoLink(name: string, type: string): string {
    if (isDocumentMerged(name, type)) {
      return mergedDocuments[name].default.documentName === currentDocumentName
        ? mergedDocuments[name].default.url
        : getUrl(mergedDocuments[name].alt);
    }

    return "";
  }

  function retryFrame(): void {
    if (bodyRef.current?.contentWindow !== null) {
      setIframeState("loading");
      bodyRef.current?.contentWindow.location.reload();
    }
  }

  function retryModalIFrame(): void {
    if (modalBodyRef.current?.contentWindow !== null) {
      setModalIframeState("loading");
      modalBodyRef.current?.contentWindow.location.reload();
    }
  }

  if (
    iframeState === "ready" &&
    bodyRef.current !== null &&
    bodyRef.current.contentDocument !== null &&
    bodyRef.current.contentDocument.title.toLowerCase().includes("error")
  ) {
    setIframeState("error");
  }

  if (
    modalIframeState === "ready" &&
    modalBodyRef.current !== null &&
    modalBodyRef.current.contentDocument !== null &&
    modalBodyRef.current.contentDocument.title.toLowerCase().includes("error")
  ) {
    setModalIframeState("error");
  }

  const glyphSize: number = Math.min(bodySize.height, bodySize.width) / 2;
  const glyphSizeTop: number =
    headSize.height + glyphPadding + glyphSize / 2 - fontSize;

  const track: () => void = useCallback((): void => {
    mixpanelTrack("DownloadGraphic", { currentDocumentName, entity });
  }, [currentDocumentName, entity]);

  useEffect((): void => {
    if (iframeState === "error" && retries < MAX_RETRIES) {
      setTimeout((): void => {
        secureStore.removeBlob(
          buildUrl(
            {
              ...props,
              documentName: currentDocumentName,
              subject: subjectName,
            },
            bodySize,
            subjectName,
            currentDocumentName
          )
        );
        setRetries((value: number): number => value + 1);
        retryFrame();
      }, DELAY_BETWEEN_RETRIES_MS);
    }
    if (modalIframeState === "error" && modalRetries < MAX_RETRIES) {
      setTimeout((): void => {
        secureStore.removeBlob(
          buildUrl(
            {
              ...props,
              documentName: currentDocumentName,
              subject: subjectName,
            },
            modalSize,
            subjectName,
            currentDocumentName
          )
        );
        setModalRetries((value: number): number => value + 1);
        retryModalIFrame();
      }, DELAY_BETWEEN_RETRIES_MS);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [iframeState, modalIframeState]);

  return (
    <React.Fragment>
      <Modal
        headerTitle={
          <div className={"w-100"}>
            <div className={styles.titleBar}>
              {currentTitle}
              <ButtonToolbar className={"f5"}>
                <FilterButton
                  changeToAll={changeToAll}
                  changeToAlternative={changeToAlternative}
                  changeToDefault={changeToDefault}
                  changeToNinety={changeToNinety}
                  changeToThirtyDays={changeTothirtyDays}
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
                      {
                        ...props,
                        documentName: currentDocumentName,
                        subject: subjectName,
                      },
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
            style={{
              opacity: modalIframeState === "ready" ? 1 : 0,
            }}
            title={currentTitle}
          />
          {modalIframeState !== "ready" && (
            <div
              className={styles.loadingComponent}
              style={{
                fontSize: glyphSize,
                top: glyphSizeTop,
              }}
            >
              {modalIframeState === "loading" ? (
                <FontAwesomeIcon icon={faHourglassHalf} />
              ) : (
                <div />
              )}
            </div>
          )}
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
                  {currentTitle}
                  {expanded &&
                    !reportMode &&
                    fullSize.width > minWidthToShowButtons && (
                      <ButtonGroup className={"fr"}>
                        <FilterButton
                          changeToAll={changeToAll}
                          changeToAlternative={changeToAlternative}
                          changeToDefault={changeToDefault}
                          changeToNinety={changeToNinety}
                          changeToThirtyDays={changeTothirtyDays}
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
                              {
                                ...props,
                                documentName: currentDocumentName,
                                subject: subjectName,
                              },
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
                loading={reportMode ? "eager" : "lazy"}
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
                title={currentTitle}
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
