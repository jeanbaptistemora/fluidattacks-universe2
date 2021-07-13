import _ from "lodash";
import type { SelectHTMLAttributes } from "react";
import React from "react";
import type { WrappedFieldProps } from "redux-form";

import { ValidationError } from "utils/forms/fields/styles";
import style from "utils/forms/index.css";

interface IDropdownProps
  extends WrappedFieldProps,
    SelectHTMLAttributes<HTMLSelectElement> {
  children?: React.ReactNode;
}

const Dropdown: React.FC<IDropdownProps> = (
  props: IDropdownProps
): JSX.Element => {
  const { disabled, input, meta, children } = props;
  const { initial, touched, error } = meta;
  const { name, onChange } = input;

  function handleDropdownChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    onChange((event.target as HTMLSelectElement).value);
  }

  return (
    <React.Fragment>
      <select
        className={style["form-control"]}
        defaultValue={initial}
        disabled={disabled}
        name={name}
        onChange={handleDropdownChange}
      >
        {children}
      </select>
      {touched && !_.isUndefined(error) && (
        <ValidationError id={"validationError"}>
          {error as string}
        </ValidationError>
      )}
    </React.Fragment>
  );
};
// eslint-disable-next-line fp/no-mutation
Dropdown.defaultProps = {
  children: "",
};

export { Dropdown };
