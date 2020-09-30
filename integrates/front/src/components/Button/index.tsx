/* eslint-disable react/forbid-component-props, react/jsx-props-no-spreading,
   @typescript-eslint/no-unused-vars
  --------
  We need className to override default styles, props spreading in
  order to pass down props to react-bootstrap Button and no unused
  vars to allow the declaration of the new button css style.
*/
import { Button } from "react-bootstrap";
import React from "react";
import style from "components/Button/index.css";
import styled, { StyledComponent } from "styled-components";

const _StyledButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs(
  (
    props: React.ButtonHTMLAttributes<HTMLButtonElement>
  ): {
    className: string;
    type: "submit" | "reset" | "button";
  } => ({
    className:
      "b--bd b--bh b--red ba bg-bd bg-bh bg-white br0 cna-bd color-bd color-bh " +
      "f2-5 fw100 ml2 montserrat o-bd ph3 pv2-5 red svg-box ws-normal",
    type: props.type ?? "button",
  })
)``;

const button: React.FC<Button.ButtonProps> = (
  props: Readonly<Button.ButtonProps>
): JSX.Element => <Button className={style.button} {...props} />;

export { button as Button };
