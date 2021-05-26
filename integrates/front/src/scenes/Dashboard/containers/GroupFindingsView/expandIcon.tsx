import { faAngleDown, faAngleUp } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import type {
  ExpandColumnRendererProps,
  ExpandHeaderColumnRenderer,
} from "react-bootstrap-table-next";

const renderExpandIcon = ({
  expanded,
}: ExpandColumnRendererProps): JSX.Element =>
  expanded ? (
    <FontAwesomeIcon icon={faAngleUp} />
  ) : (
    <FontAwesomeIcon icon={faAngleDown} />
  );

const renderHeaderExpandIcon = ({
  isAnyExpands,
}: ExpandHeaderColumnRenderer): JSX.Element =>
  isAnyExpands ? (
    <FontAwesomeIcon icon={faAngleUp} />
  ) : (
    <FontAwesomeIcon icon={faAngleDown} />
  );

export { renderExpandIcon, renderHeaderExpandIcon };
