/* eslint-disable react/forbid-component-props
  --------
  We need className to override default styles from react-bootstrap.
  */
import { IGraphicProps } from "../../types";
import React from "react";
import _ from "lodash";
import styles from "./index.css";
import {
  Button,
  ButtonGroup,
  Glyphicon,
  Grid,
  Modal,
  Panel,
  Row,
} from "react-bootstrap";
import {
  ISecureStore,
  secureStoreContext,
} from "../../../utils/secureStore/index";
import useComponentSize, { ComponentSize } from "@rehooks/component-size";

const glyphPadding: number = 15;
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

  const url: URL = new URL("/integrates/graphic", window.location.origin);
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
  const { bsHeight, footer, reportMode, subject, title } = props;

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

  const secureStore: ISecureStore = React.useContext(secureStoreContext);

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
  const glyphSizeTop: number = headSize.height + glyphPadding + glyphSize / 2;

  return (
    <React.Fragment>
      <Modal
        backdrop={true}
        bsSize={"large"}
        dialogClassName={styles.modalDialog}
        onHide={frameOnFullScreenExit}
        show={fullScreen}
      >
        <Modal.Header>
          <Modal.Title>
            <Grid fluid={true}>
              <Row>
                <div className={styles.titleBar}>
                  {title}
                  <div className={styles.buttonGroup}>
                    <ButtonGroup bsSize={"small"}>
                      <Button
                        download={buildFileName(modalSize)}
                        href={buildUrl(props, modalSize)}
                        rel={"noopener noreferrer"}
                        target={"_blank"}
                      >
                        <Glyphicon glyph={"save"} />
                      </Button>
                      <Button onClick={modalFrameOnRefresh}>
                        <Glyphicon glyph={"refresh"} />
                      </Button>
                      <Button onClick={frameOnFullScreenExit}>
                        <Glyphicon glyph={"remove"} />
                      </Button>
                    </ButtonGroup>
                  </div>
                </div>
              </Row>
            </Grid>
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
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
        </Modal.Body>
        {!_.isUndefined(footer) && (
          <Modal.Footer>
            <div className={styles.panelFooter}>{footer}</div>
          </Modal.Footer>
        )}
      </Modal>
      <div ref={fullRef}>
        <Panel
          expanded={expanded}
          onMouseEnter={panelOnMouseEnter}
          onMouseLeave={panelOnMouseLeave}
        >
          <div ref={headRef}>
            <Panel.Heading className={styles.panelTitle}>
              <Panel.Title>
                <div className={styles.titleBar}>
                  <Grid fluid={true}>
                    <Row>
                      {title}
                      {expanded &&
                        !reportMode &&
                        fullSize.width > minWidthToShowButtons && (
                          <div className={styles.buttonGroup}>
                            <ButtonGroup bsSize={"small"}>
                              <Button
                                download={buildFileName(bigGraphicSize)}
                                href={buildUrl(props, bigGraphicSize)}
                                rel={"noopener noreferrer"}
                                target={"_blank"}
                              >
                                <Glyphicon glyph={"save"} />
                              </Button>
                              <Button onClick={frameOnRefresh}>
                                <Glyphicon glyph={"refresh"} />
                              </Button>
                              <Button onClick={frameOnFullScreen}>
                                <Glyphicon glyph={"fullscreen"} />
                              </Button>
                            </ButtonGroup>
                          </div>
                        )}
                    </Row>
                  </Grid>
                </div>
              </Panel.Title>
            </Panel.Heading>
            <hr className={styles.tinyLine} />
          </div>
          <Panel.Body>
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
                  <Glyphicon
                    glyph={iframeState === "loading" ? "hourglass" : "wrench"}
                  />
                </div>
              )}
            </div>
          </Panel.Body>
          {!_.isUndefined(footer) && (
            <Panel.Collapse>
              <Panel.Footer className={styles.panelFooter}>
                {footer}
              </Panel.Footer>
            </Panel.Collapse>
          )}
        </Panel>
      </div>
    </React.Fragment>
  );
};
