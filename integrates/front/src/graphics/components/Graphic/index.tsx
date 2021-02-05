/* eslint-disable react/forbid-component-props
  --------
  We need className to override default styles from react-bootstrap.
  */
import type { ComponentSize } from "@rehooks/component-size";
import { Glyphicon } from "react-bootstrap";
import type { IGraphicProps } from "graphics/types";
import type { ISecureStoreConfig } from "utils/secureStore";
import { Modal } from "components/Modal";
import React from "react";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import { secureStoreContext } from "utils/secureStore";
import styles from "graphics/components/Graphic/index.css";
import { translate } from "utils/translations/translate";
import useComponentSize from "@rehooks/component-size";
import {
  ButtonGroup,
  GraphicButton,
  GraphicPanelCollapse,
  GraphicPanelCollapseBody,
  GraphicPanelCollapseFooter,
  GraphicPanelCollapseHeader,
} from "styles/styledComponents";

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
  size: IComponentSizeProps
): string {
  const roundedHeight: number =
    pixelsSensitivity * Math.floor(size.height / pixelsSensitivity);
  const roundedWidth: number =
    pixelsSensitivity * Math.floor(size.width / pixelsSensitivity);

  const url: URL = new URL("/graphic", window.location.origin);
  url.searchParams.set("documentName", props.documentName);
  url.searchParams.set("documentType", props.documentType);
  url.searchParams.set("entity", props.entity);
  url.searchParams.set("generatorName", props.generatorName);
  url.searchParams.set("generatorType", props.generatorType);
  url.searchParams.set("height", roundedHeight.toString());
  url.searchParams.set("subject", props.subject);
  url.searchParams.set("width", roundedWidth.toString());

  return url.toString();
}

export const Graphic: React.FC<IGraphicProps> = (
  props: Readonly<IGraphicProps>
): JSX.Element => {
  const { bsHeight, className, footer, reportMode, subject, title } = props;

  // Hooks
  const fullRef: React.MutableRefObject<HTMLDivElement | null> = React.useRef(
    null
  );
  const headRef: React.MutableRefObject<HTMLDivElement | null> = React.useRef(
    null
  );
  const bodyRef: React.MutableRefObject<HTMLIFrameElement | null> = React.useRef(
    null
  );
  const modalRef: React.MutableRefObject<HTMLIFrameElement | null> = React.useRef(
    null
  );
  const modalBodyRef: React.MutableRefObject<HTMLIFrameElement | null> = React.useRef(
    null
  );

  // More hooks
  const fullSize: ComponentSize = useComponentSize(fullRef);
  const headSize: ComponentSize = useComponentSize(headRef);
  const bodySize: ComponentSize = useComponentSize(bodyRef);
  const modalSize: ComponentSize = useComponentSize(modalBodyRef);

  const [expanded, setExpanded] = React.useState(reportMode);
  const [fullScreen, setFullScreen] = React.useState(false);
  const [iframeState, setIframeState] = React.useState("loading");

  const secureStore: ISecureStoreConfig = React.useContext(secureStoreContext);

  // Yet more hooks
  const iframeSrc: string = React.useMemo(
    (): string => secureStore.retrieveBlob(buildUrl(props, bodySize)),
    [bodySize, props, secureStore]
  );
  const modalIframeSrc: string = React.useMemo(
    (): string => secureStore.retrieveBlob(buildUrl(props, modalSize)),
    [modalSize, props, secureStore]
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
    return `${subject}-${title}-${size.width}x${size.height}.html`;
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

  const track: () => void = React.useCallback((): void => {
    const { documentName, entity } = props;
    mixpanel.track("DownloadGraphic", { documentName, entity });
  }, [props]);

  return (
    <React.Fragment>
      <Modal
        headerTitle={
          <div className={"w-100"}>
            <div className={styles.titleBar}>
              {title}
              <ButtonGroup className={"fr"}>
                <GraphicButton>
                  <a
                    className={"g-a"}
                    download={buildFileName(modalSize)}
                    href={buildUrl(props, modalSize)}
                    onClick={track}
                    rel={"noopener noreferrer"}
                    target={"_blank"}
                  >
                    <Glyphicon glyph={"save"} />
                  </a>
                </GraphicButton>
                <GraphicButton onClick={modalFrameOnRefresh}>
                  <Glyphicon glyph={"refresh"} />
                </GraphicButton>
                <GraphicButton onClick={frameOnFullScreenExit}>
                  <Glyphicon glyph={"remove"} />
                </GraphicButton>
              </ButtonGroup>
            </div>
          </div>
        }
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
          <div ref={headRef}>
            <GraphicPanelCollapseHeader>
              <div className={styles.titleBar}>
                <div className={"w-100"}>
                  {title}
                  {expanded &&
                    !reportMode &&
                    fullSize.width > minWidthToShowButtons && (
                      <ButtonGroup className={"fr"}>
                        <GraphicButton>
                          <a
                            className={"g-a"}
                            download={buildFileName(bigGraphicSize)}
                            href={buildUrl(props, bigGraphicSize)}
                            onClick={track}
                            rel={"noopener noreferrer"}
                            target={"_blank"}
                          >
                            <Glyphicon glyph={"save"} />
                          </a>
                        </GraphicButton>
                        <GraphicButton onClick={frameOnRefresh}>
                          <Glyphicon glyph={"refresh"} />
                        </GraphicButton>
                        <GraphicButton onClick={frameOnFullScreen}>
                          <Glyphicon glyph={"fullscreen"} />
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
                    <Glyphicon glyph={"hourglass"} />
                  ) : (
                    <React.Fragment>
                      <Glyphicon glyph={"wrench"} />
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
            <GraphicPanelCollapseFooter> {footer} </GraphicPanelCollapseFooter>
          )}
        </GraphicPanelCollapse>
      </div>
    </React.Fragment>
  );
};
