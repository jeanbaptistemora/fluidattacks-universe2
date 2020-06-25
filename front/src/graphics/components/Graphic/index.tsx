/* eslint-disable react/forbid-component-props
  --------
  We need className to override default styles from react-bootstrap.
*/
import useComponentSize, { ComponentSize } from "@rehooks/component-size";
import _ from "lodash";
import React from "react";
import { Glyphicon, Panel } from "react-bootstrap";
import { IGraphicProps } from "../../types";
import styles from "./index.css";

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
  const containerReference: React.MutableRefObject<null> = React.useRef(null);
  const iframeReference: React.MutableRefObject<HTMLIFrameElement | null> = React.useRef(
    null
  );
  const size: ComponentSize = useComponentSize(containerReference);

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
  url.searchParams.set(
    "generatorName",
    _.isUndefined(generatorName) ? documentName : generatorName
  );
  url.searchParams.set(
    "generatorType",
    _.isUndefined(generatorType) ? documentType : generatorType
  );
  url.searchParams.set("height", size.height.toString());
  url.searchParams.set("subject", subject);
  url.searchParams.set("width", size.width.toString());

  if (
    iframeState === "ready" &&
    iframeReference.current !== null &&
    iframeReference.current.contentDocument !== null &&
    iframeReference.current.contentDocument.title
      .toLowerCase()
      .includes("error")
  ) {
    setIframeState("error");
  }

  return (
    <React.StrictMode>
      <div>
        <Panel
          expanded={expanded}
          onMouseEnter={panelOnMouseEnter}
          onMouseLeave={panelOnMouseLeave}
        >
          {_.isUndefined(title) ? undefined : (
            <Panel.Heading className={styles.panelTitle}>
              <Panel.Title>{title}</Panel.Title>
            </Panel.Heading>
          )}
          <Panel.Body>
            <div className={bsClass} ref={containerReference}>
              <iframe
                className={styles.frame}
                hidden={iframeState !== "ready"}
                onLoad={frameOnLoad}
                ref={iframeReference}
                src={url.toString()}
              />
              {iframeState === "ready" ? undefined : (
                <div
                  className={styles.loadingComponent}
                  style={{
                    fontSize: _.min([size.height / 2, size.width / 2]),
                    top: size.height / 2,
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
