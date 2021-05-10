import { faAngleDown, faAngleUp } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

interface IExpandIconProps {
  expanded: boolean;
}

export const ExpandIcon = ({ expanded }: IExpandIconProps): JSX.Element =>
  expanded ? (
    <FontAwesomeIcon icon={faAngleUp} />
  ) : (
    <FontAwesomeIcon icon={faAngleDown} />
  );
