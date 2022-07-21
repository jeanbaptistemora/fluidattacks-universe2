import { faAsterisk, faCircleInfo } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FC, ReactNode } from "react";
import React from "react";

import { Text } from "components/Text";
import { Tooltip } from "components/Tooltip";

interface ILabelProps {
  children?: ReactNode;
  htmlFor?: string;
  required?: boolean;
  tooltip?: string;
}

const Label: FC<ILabelProps> = ({
  children,
  htmlFor,
  required = false,
  tooltip,
}: Readonly<ILabelProps>): JSX.Element => (
  <label htmlFor={htmlFor}>
    {required ? (
      <FontAwesomeIcon color={"#bf0b1a"} icon={faAsterisk} size={"xs"} />
    ) : undefined}
    <Text disp={"inline-block"} mb={1} ml={required ? 1 : 0} mr={1}>
      {children}
    </Text>
    {tooltip === undefined || htmlFor === undefined ? undefined : (
      <Tooltip
        disp={"inline-block"}
        id={`${htmlFor}-tooltip`}
        place={"bottom"}
        tip={tooltip}
      >
        <FontAwesomeIcon color={"#b0b0bf"} icon={faCircleInfo} size={"sm"} />
      </Tooltip>
    )}
  </label>
);

export type { ILabelProps };
export { Label };
