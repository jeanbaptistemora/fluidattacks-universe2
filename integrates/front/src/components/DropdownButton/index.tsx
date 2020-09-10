/* eslint-disable react/forbid-component-props, react/jsx-props-no-spreading
  --------
  We need className to override default styles and props spreading in
  order to pass down props to react-bootstrap DropdownButton.
*/
import React from "react";
import style from "components/DropdownButton/index.css";
import { DropdownButton, MenuItem } from "react-bootstrap";

/*
 * They have a bug in this onSelect type
 *   https://react-bootstrap-v3.netlify.app/components/dropdowns/
 *
 * Below is the one declared in the docs and the one they actually implement
 */
interface IDropdownButtonProps
  extends Omit<DropdownButton.DropdownButtonProps, "onSelect"> {
  onSelect?: (eventKey: string) => void;
}

const dropdownButton: React.FC<IDropdownButtonProps> = (
  props: Readonly<IDropdownButtonProps>
): JSX.Element => (
  <DropdownButton
    className={style.dropdownButton}
    {...(props as DropdownButton.DropdownButtonProps)}
  />
);

export { dropdownButton as DropdownButton, MenuItem };
