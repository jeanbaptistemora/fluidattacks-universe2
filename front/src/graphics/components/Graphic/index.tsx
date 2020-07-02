/* eslint-disable react/forbid-component-props
  --------
  We need className to override default styles from react-bootstrap.
  */
import { IGraphicProps } from "../../types";
import React from "react";
import _ from "lodash";
import styles from "./index.css";
import { Glyphicon, Panel } from "react-bootstrap";
import useComponentSize, { ComponentSize } from "@rehooks/component-size";

const glyphPadding: number = 15;

export const Graphic: React.FC<IGraphicProps> = (
  props: Readonly<IGraphicProps>
): JSX.Element => {
  const {
    bsClass,
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

  const headSize: ComponentSize = useComponentSize(headRef);
  const bodySize: ComponentSize = useComponentSize(bodyRef);

  const [expanded, setExpanded] = React.useState(false);
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

  const url: URL = new URL("/integrates/graphic", window.location.origin);

  url.searchParams.set("documentName", documentName);
  url.searchParams.set("documentType", documentType);
  url.searchParams.set("entity", entity);
  url.searchParams.set("generatorName", generatorName);
  url.searchParams.set("generatorType", generatorType);
  url.searchParams.set("height", bodySize.height.toString());
  url.searchParams.set("subject", subject);
  url.searchParams.set("width", bodySize.width.toString());

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
      <div ref={fullRef}>
        <Panel
          expanded={expanded}
          onMouseEnter={panelOnMouseEnter}
          onMouseLeave={panelOnMouseLeave}
        >
          <div ref={headRef}>
            <Panel.Heading className={styles.panelTitle}>
              <Panel.Title>
                <a
                  href={url.toString()}
                  rel={"noopener noreferrer"}
                  target={"_blank"}
                >
                  {title}
                </a>
              </Panel.Title>
            </Panel.Heading>
            <hr className={styles.tinyLine} />
          </div>
          <Panel.Body>
            <div className={bsClass}>
              <iframe
                className={styles.frame}
                frameBorder={"no"}
                onLoad={frameOnLoad}
                ref={bodyRef}
                scrolling={"no"}
                src={url.toString()}
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
