import { capitalize } from "lodash";
import React, { useCallback } from "react";

import { LinkRow } from "./lintRow";

import { translate } from "utils/translations/translate";

interface ILinkFormatterProps {
  value: boolean | string | undefined;
  row: Readonly<Record<string, string>>;
  // eslint-disable-next-line react/require-default-props
  changeFunction?: (arg: Record<string, string>) => void;
}

const LinkFormatter: React.FC<ILinkFormatterProps> = ({
  value,
  row,
  changeFunction,
}: ILinkFormatterProps): JSX.Element => {
  const onClick = useCallback((): void => {
    changeFunction?.(row);
  }, [changeFunction, row]);

  const valueDefined: boolean | string = value ?? "";

  function getformatedValue(): string {
    if (typeof valueDefined === "string") {
      return valueDefined.replace("_", " ");
    } else if (valueDefined) {
      return translate.t("organization.tabs.billing.groups.managed.yes");
    }

    return translate.t("organization.tabs.billing.groups.managed.no");
  }

  const formatedValueDefined: string = getformatedValue();

  return (
    <LinkRow
      onClick={onClick}
      value={capitalize(formatedValueDefined.toLocaleLowerCase())}
    />
  );
};

export const linkFormatter = (
  value: boolean | string | undefined,
  row: Readonly<Record<string, string>>,
  changeFunction?: (arg: Record<string, string>) => void
): JSX.Element => {
  return (
    <LinkFormatter changeFunction={changeFunction} row={row} value={value} />
  );
};
