/* eslint-disable react/forbid-component-props, react/jsx-props-no-spreading
  --------
  We need className to override default styles and props spreading in
  order to pass down props to react-bootstrap DropdownButton.
*/
import React from "react";
import { default as style } from "./index.css";
import { DropdownButton, MenuItem } from "react-bootstrap";

const dropdownButton: React.FC<DropdownButton.DropdownButtonProps> = (
  props: Readonly<DropdownButton.DropdownButtonProps>
): JSX.Element => (
  <DropdownButton className={style.dropdownButton} {...props} />
);

export { dropdownButton as DropdownButton, MenuItem };
