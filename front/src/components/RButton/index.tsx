/* tslint:disable:jsx-no-lambda no-any
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 */
import React from "react";
import { Button, Glyphicon } from "react-bootstrap";
import style from "./index.css";
/**
 * Button properties
 */
interface IRButtonProps {
  bicon: string;
  bstyle: string;
  btitle: string;
  onClickButton(): void;
}

const buttonFormatter: ((value: string) => string) =
  (value: string): string => {
    let btColor: string;
    switch (value) {
      case "btn-default":
        btColor = style.btn_default;
        break;
      case "btn-primary":
        btColor = style.btn_primary;
        break;
      case "btn-success":
        btColor = style.btn_success;
        break;
      case "btn-warning":
        btColor = style.btn_warning;
        break;
      default:
        btColor = "";
    }

    return btColor;
};

/**
 * Button
 */
const button: React.FunctionComponent<IRButtonProps> =
  (props: IRButtonProps): JSX.Element => (
  <React.StrictMode>
    <Button
      className={buttonFormatter(props.bstyle)}
      onClick={(): void => {props.onClickButton(); }}
      block={true}
    >
      <Glyphicon glyph={props.bicon}/>&nbsp;{props.btitle}
    </Button>
  </React.StrictMode>
);

button.defaultProps = {
  bicon: "",
  bstyle: "",
  btitle: "",
  onClickButton: (): void => undefined,
};

export = button;
