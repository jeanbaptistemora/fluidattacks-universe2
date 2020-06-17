/* tslint:disable:jsx-no-multiline-js
 * disabling for the sake of readability
 */
import useComponentSize, { ComponentSize } from "@rehooks/component-size";
import _ from "lodash";
import React from "react";
import { Glyphicon } from "react-bootstrap";
import rd3 from "react-d3-library";
import rollbar from "../utils/rollbar";
import styles from "./index.css";
import { IGraphicProps, NodeType } from "./types";

const graphic: React.FC<IGraphicProps> = (props: IGraphicProps): JSX.Element => {
  const { bsClass, data, generator } = props;

  // Hooks
  /* tslint:disable-next-line:no-null-keyword
   * null is the right typing for this reference
   */
  const containerReference: React.MutableRefObject<null> = React.useRef(null);
  const size: ComponentSize = useComponentSize(containerReference);
  const memoizedNode: NodeType | undefined = React.useMemo(
    () => {
      let node: NodeType | undefined;

      try {
        // Attempt to generate the node
        node = generator(data, size.width, size.height);
      } catch (error) {
        // Fallback case, some things may fail so we better be prepared
        node = undefined;
        // Let us know that something happened
        rollbar.error("An error occurred loading event comments", error);
      }

      return node;
    },
    [data, size]);

  return (
    <React.StrictMode>
      <div className={bsClass} ref={containerReference}>
        {_.isUndefined(memoizedNode) ? (
          <div
            className={styles.errorComponent}
            style={{ fontSize: _.min([size.height / 2, size.width / 2]) }}
          >
            <Glyphicon glyph="fire" />
          </div>
        ) : (
          <rd3.Component data={memoizedNode} />
        )}
      </div>
    </React.StrictMode>
  );
};

export { graphic as Graphic };
