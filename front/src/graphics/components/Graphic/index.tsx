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
import useComponentSize, { ComponentSize } from "@rehooks/component-size";

const glyphPadding: number = 15;
const minWidthToShowButtons: number = 320;
const bigGraphicHeight: number = 400;
const bigGraphicWidth: number = 1000;

export const Graphic: React.FC<IGraphicProps> = (
  props: Readonly<IGraphicProps>
): JSX.Element => {
  const {
    bsHeight,
    documentName,
    documentType,
    entity,
    footer,
    generatorName,
    generatorType,
    subject,
    title,
  } = props;

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

  const fullSize: ComponentSize = useComponentSize(fullRef);
  const headSize: ComponentSize = useComponentSize(headRef);
  const bodySize: ComponentSize = useComponentSize(bodyRef);
  const modalSize: ComponentSize = useComponentSize(modalRef);

  const [expanded, setExpanded] = React.useState(false);
  const [fullScreen, setFullScreen] = React.useState(false);
  const [iframeState, setIframeState] = React.useState("loading");

  function panelOnMouseEnter(): void {
    setExpanded(true);
  }
  function panelOnMouseLeave(): void {
    setExpanded(false);
  }
  function frameOnLoad(): void {
    setIframeState("ready");
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
  function modalFrameOnRefresh(): void {
    if (modalBodyRef.current?.contentWindow !== null) {
      modalBodyRef.current?.contentWindow.location.reload();
    }
  }
  function buildFileName(width: number, height: number): string {
    return `${subject}-${title}-${width}x${height}.html`;
  }
  function buildUrl(width: number, height: number): string {
    const url: URL = new URL("/integrates/graphic", window.location.origin);

    url.searchParams.set("documentName", documentName);
    url.searchParams.set("documentType", documentType);
    url.searchParams.set("entity", entity);
    url.searchParams.set("generatorName", generatorName);
    url.searchParams.set("generatorType", generatorType);
    url.searchParams.set("height", height.toString());
    url.searchParams.set("subject", subject);
    url.searchParams.set("width", width.toString());

    return url.toString();
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
    <React.StrictMode>
      <Modal
        autoFocus={true}
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
                        download={buildFileName(
                          modalSize.width,
                          modalSize.height
                        )}
                        href={buildUrl(modalSize.width, modalSize.height)}
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
          <div ref={modalRef} style={{ height: bigGraphicHeight }}>
            <iframe
              className={styles.frame}
              frameBorder={"no"}
              ref={modalBodyRef}
              scrolling={"no"}
              src={buildUrl(modalSize.width, modalSize.height)}
            />
          </div>
        </Modal.Body>
        {_.isUndefined(footer) ? undefined : (
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
                      {expanded && fullSize.width > minWidthToShowButtons ? (
                        <div className={styles.buttonGroup}>
                          <ButtonGroup bsSize={"small"}>
                            <Button
                              download={buildFileName(
                                bigGraphicWidth,
                                bigGraphicHeight
                              )}
                              href={buildUrl(bigGraphicWidth, bigGraphicHeight)}
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
                      ) : undefined}
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
                src={buildUrl(bodySize.width, bodySize.height)}
                style={{
                  /*
                   * The element must be rendered for C3 legends to work,
                   * so lets just hide it from the user
                   */
                  opacity: iframeState === "ready" ? 1 : 0,
                }}
              />
              {iframeState === "ready" ? undefined : (
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
          {_.isUndefined(footer) ? undefined : (
            <Panel.Collapse>
              <Panel.Footer className={styles.panelFooter}>
                {footer}
              </Panel.Footer>
            </Panel.Collapse>
          )}
        </Panel>
      </div>
    </React.StrictMode>
  );
};
