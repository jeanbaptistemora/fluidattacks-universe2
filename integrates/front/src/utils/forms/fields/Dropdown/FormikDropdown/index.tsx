/* eslint-disable @typescript-eslint/prefer-readonly-parameter-types, react/forbid-component-props
  -------
  Readonly utility type does not work on deeply nested types and we need
  className to override default styles from react-bootstrap.
*/
import type { FieldProps } from "formik";
import { useField } from "formik";
import _ from "lodash";
import React from "react";

import { ValidationError } from "styles/styledComponents";
import style from "utils/forms/index.css";

interface IDropdownProps extends FieldProps {
  children?: React.ReactNode;
}

const FormikDropdown: React.FC<IDropdownProps> = (
  props: IDropdownProps
): JSX.Element => {
  const { field, children } = props;
  const { name, onChange, onBlur } = field;
  const [, meta] = useField(name);
  const { initialValue, touched, error } = meta;

  return (
    <React.Fragment>
      <select
        className={style["form-control"]}
        defaultValue={initialValue}
        name={name}
        onBlur={onBlur}
        onChange={onChange}
      >
        {children}
      </select>
      {touched && !_.isUndefined(error) && (
        <ValidationError id={"validationError"}>{error}</ValidationError>
      )}
    </React.Fragment>
  );
};
// eslint-disable-next-line fp/no-mutation
FormikDropdown.defaultProps = {
  children: "",
};

export { FormikDropdown };
