/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React, { useCallback } from "react";

interface ISuggestionItemProps {
  onChange: (value: string) => void;
  value: string;
}

export const SuggestionItem: React.FC<ISuggestionItemProps> = ({
  value,
  onChange,
}: ISuggestionItemProps): JSX.Element => {
  const handleClick = useCallback((): void => {
    onChange(value);
  }, [onChange, value]);

  return (
    <button onClick={handleClick} type={"button"}>
      <li>{value}</li>
    </button>
  );
};
