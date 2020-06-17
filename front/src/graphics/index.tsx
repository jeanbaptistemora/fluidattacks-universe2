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

/* D3 alters the DOM (a lot)
 *
 * However, that DOM is detached from the virtual DOM of React.
 *
 * This implies that changes to the DOM that D3 sees do not trigger a render
 * in the DOM of React (what the user actually sees), causing graphics
 * to be non-interactive.
 *
 * On the other hand, changes caused by props change trigger a full render,
 * which resets all interaction, causing ugly flushes to the user.
 *
 * This is a work-around that forces a virtual DOM render,
 * which copies the current state of D3's DOM into Reacts DOM so it keeps in sync.
 */
const useForcePeriodicUpdate: (intervalInSeconds: number) => void = (intervalInSeconds: number): void => {
  // A dummy state to trigger the render operation
  const [tick, setTick] = React.useState(0);

  // Triggered once component mounts
  React.useEffect(() => {
    const forceUpdate: () => void = (): void => {
      setTick(tick + 1);
    };
    const intervalHandler: NodeJS.Timeout = setInterval(forceUpdate, intervalInSeconds);

    // Triggered once component un-mounts
    return () => {
      clearInterval(intervalHandler);
    };
  });
};

const graphic: React.FC<IGraphicProps> = (props: IGraphicProps): JSX.Element => {
  const { bsClass, data, generator } = props;

  // Hooks
  useForcePeriodicUpdate(1);
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
        rollbar.error("An error occurred loading a d3 document", error);
      }

      return node;
    },
    [size.width, size.height],
  );

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
