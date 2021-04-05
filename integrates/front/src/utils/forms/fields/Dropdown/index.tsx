/* eslint-disable @typescript-eslint/prefer-readonly-parameter-types, react/forbid-component-props
  -------
  Readonly utility type does not work on deeply nested types and we need
  className to override default styles from react-bootstrap.
*/
import _ from "lodash";
import React from "react";
import type { WrappedFieldProps } from "redux-form";

import { ValidationError } from "styles/styledComponents";
import style from "utils/forms/index.css";

interface IDropdownProps extends WrappedFieldProps {
  children?: React.ReactNode;
}

const Dropdown: React.FC<IDropdownProps> = (
  props: IDropdownProps
): JSX.Element => {
  const { input, meta, children } = props;
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
