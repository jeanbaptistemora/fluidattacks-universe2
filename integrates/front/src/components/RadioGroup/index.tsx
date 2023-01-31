import _ from "lodash";
import React, { useCallback, useState } from "react";

import { Radio, RadioLabel, SwitchItem } from "styles/styledComponents";

interface IRadioGroupProps {
  selected: (value: unknown) => void;
  labels: string[];
  onSelect?: (checked: boolean) => void;
  initialState?: string;
  switchColor?: string;
}

const RadioGroup: React.FC<IRadioGroupProps> = (
  props: Readonly<IRadioGroupProps>
): JSX.Element => {
  const {
    selected,
    labels,
    initialState = "",
    onSelect,
    switchColor = "bg-switch b-switch white",
  } = props;

  const [select, setSelect] = useState(initialState);

  const handleSelectChange = useCallback(
    (label: string): (() => void) =>
      (): void => {
        setSelect(label);
        if (label === labels[0]) {
          if (!_.isUndefined(onSelect)) {
            onSelect(true);
          }
          selected(true);
        } else {
          if (!_.isUndefined(onSelect)) {
            onSelect(false);
          }
          selected(false);
        }
      },
    [labels, onSelect, selected]
  );

  const listItems: JSX.Element[] = labels.map(
    (label): JSX.Element => (
      <React.Fragment key={label}>
        <Radio
          aria-label={label}
          checked={select === label}
          onChange={handleSelectChange(label)}
          value={label}
        />
        <RadioLabel
          id={label}
          onClick={handleSelectChange(label)}
          theme={{ color: switchColor, on: select === label }}
        >
          {label}
        </RadioLabel>
      </React.Fragment>
    )
  );

  return <SwitchItem>{listItems}</SwitchItem>;
};

export type { IRadioGroupProps };
export { RadioGroup };
