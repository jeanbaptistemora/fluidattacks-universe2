/* eslint-disable react/forbid-component-props, react/jsx-props-no-spreading
  --------
  We need className to override default styles and props spreading in
  order to pass down props to react-bootstrap Button.
*/
import React from "react";
import { Button } from "react-bootstrap";
import { default as style } from "./index.css";

const button: React.FC<Button.ButtonProps> = (
  props: Readonly<Button.ButtonProps>
): JSX.Element => <Button className={style.button} {...props} />;

export { button as Button };
