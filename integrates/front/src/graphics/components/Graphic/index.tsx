/* eslint-disable react/forbid-component-props
  --------
  We need className to override default styles from react-bootstrap.
  */
import {
  faDownload,
  faExpandArrowsAlt,
  faFileCsv,
  faHourglassHalf,
  faInfoCircle,
  faSyncAlt,
  faWrench,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { ComponentSize } from "@rehooks/component-size";
import useComponentSize from "@rehooks/component-size";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, {
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";

import { GraphicIframe } from "./styles";

import { ExternalLink } from "components/ExternalLink";
import { Modal } from "components/Modal";
import { Tooltip } from "components/Tooltip/index";
import type { IDocumentValues } from "graphics/components/Graphic/ctx";
import {
  allowedDocumentNames,
  allowedDocumentTypes,
  mergedDocuments,
} from "graphics/components/Graphic/ctx";
import { FilterButton } from "graphics/components/Graphic/filterButton";
import styles from "graphics/components/Graphic/index.css";
import { hasIFrameError } from "graphics/components/Graphic/utils";
import type { IGraphicProps } from "graphics/types";
import {
  GraphicButton,
  GraphicPanelCollapse,
  GraphicPanelCollapseBody,
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
const minModalSize: number = 40;
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

function buildCsvUrl(
  props: IReadonlyGraphicProps,
  subjectName: string,
  documentName: string
): string {
  const url: URL = new URL("/graphic-csv", window.location.origin);
  url.searchParams.set("documentName", documentName);
  url.searchParams.set("documentType", props.documentType);
  url.searchParams.set("entity", props.entity);
  url.searchParams.set("generatorName", props.generatorName);
  url.searchParams.set("generatorType", props.generatorType);
  url.searchParams.set("subject", subjectName);

  return url.toString();
}

// eslint-disable-next-line complexity
export const Graphic: React.FC<IGraphicProps> = (
  props: Readonly<IGraphicProps>
): JSX.Element => {
  const {
    bsHeight,
    className,
    shouldDisplayAll = true,
    documentName,
    documentType,
    entity,
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
  const [iFrameKey, setIFrameKey] = useState(0);
  const [modalIFrameKey, setModalIFrameKey] = useState(0);

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

  const minModalWidth = useMemo((): number => {
    const roundedWidth: number =
      pixelsSensitivity * Math.floor(bodySize.width / pixelsSensitivity);

    return roundedWidth + minModalSize;
  }, [bodySize]);

  const panelOnMouseEnter = useCallback((): void => {
    setExpanded(true);
  }, []);
  const panelOnMouseLeave = useCallback((): void => {
    setExpanded(reportMode);
  }, [reportMode]);
  const frameOnLoad = useCallback((): void => {
    setIframeState("ready");
    secureStore.storeIframeContent(bodyRef);
  }, [secureStore]);
  const frameOnFullScreen = useCallback((): void => {
    setFullScreen(true);
  }, []);
  const frameOnFullScreenExit = useCallback((): void => {
    setFullScreen(false);
  }, []);
  const frameOnRefresh = useCallback((): void => {
    if (bodyRef.current?.contentWindow !== null) {
      setRetries(0);
      setIframeState("loading");
      setIFrameKey((value: number): number => {
        if (value >= DELAY_BETWEEN_RETRIES_MS) {
          return 0;
        }

        return value + 1;
      });
    }
  }, []);
  const modalFrameOnLoad = useCallback((): void => {
    setModalIframeState("ready");
    secureStore.storeIframeContent(modalBodyRef);
  }, [secureStore]);
  const modalFrameOnRefresh = useCallback((): void => {
    if (modalBodyRef.current?.contentWindow !== null) {
      setModalIframeState("loading");
      setModalRetries(0);
      setModalIFrameKey((value: number): number => {
        if (value >= DELAY_BETWEEN_RETRIES_MS) {
          return 0;
        }

        return value + 1;
      });
    }
  }, []);
  function buildFileName(size: IComponentSizeProps): string {
    return `${currentTitle}-${subject}-${size.width}x${size.height}.html`;
  }
  const csvFileName: string = useMemo(
    (): string => `${subject}-${currentTitle}.csv`,
    [currentTitle, subject]
  );
  const shouldDisplayExtraButtons: boolean = useMemo((): boolean => {
    return expanded && !reportMode && fullSize.width > minWidthToShowButtons;
  }, [expanded, reportMode, fullSize.width]);

  function changeTothirtyDays(): void {
    setSubjectName(`${subject}_30`);
    frameOnRefresh();
  }

  const changeToNinety = useCallback((): void => {
    setSubjectName(`${subject}_90`);
    frameOnRefresh();
  }, [frameOnRefresh, subject]);

  function changeToSixtyDays(): void {
    setSubjectName(`${subject}_60`);
    frameOnRefresh();
  }
  function changeToOneHundredEighty(): void {
    setSubjectName(`${subject}_180`);
    frameOnRefresh();
  }

  const changeToAll = useCallback((): void => {
    setSubjectName(subject);
    frameOnRefresh();
  }, [frameOnRefresh, subject]);

  const changeToDefault = useCallback((): void => {
    setCurrentDocumentName(documentName);
    setCurrentTitle(title);
    frameOnRefresh();
  }, [documentName, frameOnRefresh, title]);

  const changeToAlternative = useCallback(
    (index: number): void => {
      if (_.includes(Object.keys(mergedDocuments), documentName)) {
        setCurrentDocumentName(
          mergedDocuments[documentName].alt[index].documentName
        );
        setCurrentTitle(mergedDocuments[documentName].alt[index].title);
        frameOnRefresh();
      }
    },
    [documentName, frameOnRefresh]
  );

  function isDocumentAllowed(name: string, type: string): boolean {
    return (
      _.includes(allowedDocumentNames, name) &&
      _.includes(allowedDocumentTypes, type)
    );
  }
  const isDocumentMerged = useCallback(
    (name: string, type: string): boolean => {
      return (
        _.includes(Object.keys(mergedDocuments), name) &&
        mergedDocuments[name].documentType === type
      );
    },
    []
  );
  const getUrl = useCallback(
    (alternatives: IDocumentValues[]): string => {
      return alternatives.reduce(
        (url: string, alternative: IDocumentValues): string =>
          alternative.documentName === currentDocumentName
            ? alternative.url
            : url,
        ""
      );
    },
    [currentDocumentName]
  );

  const getAdditionalInfoLink = useCallback(
    (name: string, type: string): string => {
      if (isDocumentMerged(name, type)) {
        return mergedDocuments[name].default.documentName ===
          currentDocumentName
          ? mergedDocuments[name].default.url
          : getUrl(mergedDocuments[name].alt);
      }

      return "";
    },
    [currentDocumentName, getUrl, isDocumentMerged]
  );

  const shouldDisplayUrl: boolean = useMemo(
    (): boolean =>
      isDocumentMerged(documentName, documentType)
        ? !_.isEmpty(getAdditionalInfoLink(documentName, documentType))
        : true,
    [documentName, documentType, getAdditionalInfoLink, isDocumentMerged]
  );

  function retryFrame(): void {
    if (bodyRef.current?.contentWindow !== null) {
      setIframeState("loading");
      setIFrameKey((value: number): number => {
        if (value >= DELAY_BETWEEN_RETRIES_MS) {
          return 0;
        }

        return value + 1;
      });
    }
  }

  function retryModalIFrame(): void {
    if (modalBodyRef.current?.contentWindow !== null) {
      setModalIframeState("loading");
      setModalIFrameKey((value: number): number => {
        if (value >= DELAY_BETWEEN_RETRIES_MS) {
          return 0;
        }

        return value + 1;
      });
    }
  }

  if (iframeState === "ready" && hasIFrameError(bodyRef)) {
    setIframeState("error");
  }

  if (modalIframeState === "ready" && hasIFrameError(modalBodyRef)) {
    setModalIframeState("error");
  }

  const glyphSize: number = Math.min(bodySize.height, bodySize.width) / 2;
  const glyphSizeTop: number =
    headSize.height + glyphPadding + glyphSize / 2 - fontSize;

  const track: () => void = useCallback((): void => {
    mixpanel.track("DownloadGraphic", { currentDocumentName, entity });
  }, [currentDocumentName, entity]);

  const trackCsv: () => void = useCallback((): void => {
    mixpanel.track("DownloadCsvGraphic", { currentDocumentName, entity });
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
        minWidth={minModalWidth}
        onClose={frameOnFullScreenExit}
        open={fullScreen}
        title={
          <div className={"flex justify-between w-100"}>
            <div className={`${styles.titleBar} w-50`}>{currentTitle}</div>
            <div className={"w-50 pr2"}>
              <div className={"f6 fr"}>
                <FilterButton
                  changeToAll={changeToAll}
                  changeToAlternative={changeToAlternative}
                  changeToDefault={changeToDefault}
                  changeToNinety={changeToNinety}
                  changeToOneHundredEighty={
                    shouldDisplayAll ? undefined : changeToOneHundredEighty
                  }
                  changeToSixtyDays={
                    shouldDisplayAll ? undefined : changeToSixtyDays
                  }
                  changeToThirtyDays={
                    shouldDisplayAll ? changeTothirtyDays : changeToAll
                  }
                  currentDocumentName={currentDocumentName}
                  documentName={documentName}
                  documentNameFilter={isDocumentMerged(
                    documentName,
                    documentType
                  )}
                  shouldDisplayAll={shouldDisplayAll}
                  subject={subject}
                  subjectName={subjectName}
                  timeFilter={isDocumentAllowed(documentName, documentType)}
                />
                {!_.isUndefined(infoLink) && shouldDisplayUrl ? (
                  <ExternalLink
                    href={
                      infoLink +
                      getAdditionalInfoLink(documentName, documentType)
                    }
                  >
                    <Tooltip
                      disp={"inline-block"}
                      id={"information_button_tooltip"}
                      tip={translate.t(
                        "analytics.buttonToolbar.information.tooltip"
                      )}
                    >
                      <GraphicButton>
                        <FontAwesomeIcon icon={faInfoCircle} />
                      </GraphicButton>
                    </Tooltip>
                  </ExternalLink>
                ) : undefined}
                <ExternalLink
                  download={csvFileName}
                  href={buildCsvUrl(
                    {
                      ...props,
                      documentName: currentDocumentName,
                      subject: subjectName,
                    },
                    subjectName,
                    currentDocumentName
                  )}
                  onClick={trackCsv}
                >
                  <Tooltip
                    disp={"inline-block"}
                    id={"csv_file_button_tooltip"}
                    tip={translate.t("analytics.buttonToolbar.fileCsv.tooltip")}
                  >
                    <GraphicButton>
                      <FontAwesomeIcon icon={faFileCsv} />
                    </GraphicButton>
                  </Tooltip>
                </ExternalLink>
                <ExternalLink
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
                >
                  <Tooltip
                    disp={"inline-block"}
                    id={"download_button_tooltip"}
                    tip={translate.t(
                      "analytics.buttonToolbar.download.tooltip"
                    )}
                  >
                    <GraphicButton>
                      <FontAwesomeIcon icon={faDownload} />
                    </GraphicButton>
                  </Tooltip>
                </ExternalLink>
                <Tooltip
                  disp={"inline-block"}
                  id={"refresh_button_tooltip"}
                  tip={translate.t("analytics.buttonToolbar.refresh.tooltip")}
                >
                  <GraphicButton onClick={modalFrameOnRefresh}>
                    <FontAwesomeIcon icon={faSyncAlt} />
                  </GraphicButton>
                </Tooltip>
              </div>
            </div>
          </div>
        }
      >
        <div ref={modalRef} style={{ height: bigGraphicSize.height }}>
          <GraphicIframe
            frameBorder={"no"}
            key={modalIFrameKey}
            onLoad={modalFrameOnLoad}
            ref={modalBodyRef}
            sandbox={"allow-modals, allow-scripts"}
            scrolling={"no"}
            src={modalIframeSrc}
            style={{
              opacity: modalIframeState === "ready" ? 1 : 0,
            }}
            title={currentTitle}
          />
          {modalIframeState === "ready" ? undefined : (
            <div
              className={styles.loadingComponent}
              style={{
                fontSize: glyphSize,
                top: glyphSizeTop,
              }}
            >
              {modalIframeState === "loading" ? (
                <div className={"pt5"}>
                  <FontAwesomeIcon icon={faHourglassHalf} />
                </div>
              ) : (
                <div />
              )}
            </div>
          )}
        </div>
      </Modal>
      <div ref={fullRef}>
        <GraphicPanelCollapse
          className={className}
          onMouseEnter={panelOnMouseEnter}
          onMouseLeave={panelOnMouseLeave}
        >
          <div className={"report-title-pad"} ref={headRef}>
            <GraphicPanelCollapseHeader>
              <div className={` ${styles.titleBar} w-100`}>
                <div
                  className={
                    "w-100 report-title flex flex-wrap justify-between items-center"
                  }
                >
                  <div>{currentTitle}</div>
                  {shouldDisplayExtraButtons ? (
                    <div>
                      <FilterButton
                        changeToAll={changeToAll}
                        changeToAlternative={changeToAlternative}
                        changeToDefault={changeToDefault}
                        changeToNinety={changeToNinety}
                        changeToOneHundredEighty={
                          shouldDisplayAll
                            ? undefined
                            : changeToOneHundredEighty
                        }
                        changeToSixtyDays={
                          shouldDisplayAll ? undefined : changeToSixtyDays
                        }
                        changeToThirtyDays={
                          shouldDisplayAll ? changeTothirtyDays : changeToAll
                        }
                        currentDocumentName={currentDocumentName}
                        documentName={documentName}
                        documentNameFilter={isDocumentMerged(
                          documentName,
                          documentType
                        )}
                        shouldDisplayAll={shouldDisplayAll}
                        subject={subject}
                        subjectName={subjectName}
                        timeFilter={isDocumentAllowed(
                          documentName,
                          documentType
                        )}
                      />
                      {!_.isUndefined(infoLink) && shouldDisplayUrl ? (
                        <ExternalLink
                          href={
                            infoLink +
                            getAdditionalInfoLink(documentName, documentType)
                          }
                        >
                          <Tooltip
                            disp={"inline-block"}
                            id={"information_button_tooltip"}
                            tip={translate.t(
                              "analytics.buttonToolbar.information.tooltip"
                            )}
                          >
                            <GraphicButton>
                              <FontAwesomeIcon icon={faInfoCircle} />
                            </GraphicButton>
                          </Tooltip>
                        </ExternalLink>
                      ) : undefined}
                      {documentType === "textBox" ? undefined : (
                        <React.Fragment>
                          <ExternalLink
                            download={csvFileName}
                            href={buildCsvUrl(
                              {
                                ...props,
                                documentName: currentDocumentName,
                                subject: subjectName,
                              },
                              subjectName,
                              currentDocumentName
                            )}
                            onClick={trackCsv}
                          >
                            <Tooltip
                              disp={"inline-block"}
                              id={"csv_file_button_tooltip"}
                              tip={translate.t(
                                "analytics.buttonToolbar.fileCsv.tooltip"
                              )}
                            >
                              <GraphicButton>
                                <FontAwesomeIcon icon={faFileCsv} />
                              </GraphicButton>
                            </Tooltip>
                          </ExternalLink>
                          <ExternalLink
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
                          >
                            <Tooltip
                              disp={"inline-block"}
                              id={"download_button_tooltip"}
                              tip={translate.t(
                                "analytics.buttonToolbar.download.tooltip"
                              )}
                            >
                              <GraphicButton>
                                <FontAwesomeIcon icon={faDownload} />
                              </GraphicButton>
                            </Tooltip>
                          </ExternalLink>
                          <Tooltip
                            disp={"inline-block"}
                            id={"refresh_button_tooltip"}
                            tip={translate.t(
                              "analytics.buttonToolbar.refresh.tooltip"
                            )}
                          >
                            <GraphicButton onClick={frameOnRefresh}>
                              <FontAwesomeIcon icon={faSyncAlt} />
                            </GraphicButton>
                          </Tooltip>
                          <Tooltip
                            disp={"inline-block"}
                            id={"expand_button_tooltip"}
                            tip={translate.t(
                              "analytics.buttonToolbar.expand.tooltip"
                            )}
                          >
                            <GraphicButton onClick={frameOnFullScreen}>
                              <FontAwesomeIcon icon={faExpandArrowsAlt} />
                            </GraphicButton>
                          </Tooltip>
                        </React.Fragment>
                      )}
                    </div>
                  ) : undefined}
                </div>
              </div>
            </GraphicPanelCollapseHeader>
            <hr className={styles.tinyLine} />
          </div>
          <GraphicPanelCollapseBody>
            <div style={{ height: bsHeight }}>
              <GraphicIframe
                frameBorder={"no"}
                key={iFrameKey}
                loading={reportMode ? "eager" : "lazy"}
                onLoad={frameOnLoad}
                ref={bodyRef}
                sandbox={"allow-scripts"}
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
              {iframeState === "ready" ? undefined : (
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
                      <p className={"black f5 ma0 tc"}>
                        {translate.t("analytics.emptyChart.text")}
                      </p>
                    </React.Fragment>
                  )}
                </div>
              )}
            </div>
          </GraphicPanelCollapseBody>
        </GraphicPanelCollapse>
      </div>
    </React.Fragment>
  );
};
