import React from "react";
import { Button } from "react-bootstrap";
import { default as style } from "./index.css";

const button: React.FunctionComponent<Button.ButtonProps> = (props: Button.ButtonProps): JSX.Element => (
  <React.StrictMode>
    <Button className={style.button} {...props} />
  </React.StrictMode>
);

export { button as Button };
