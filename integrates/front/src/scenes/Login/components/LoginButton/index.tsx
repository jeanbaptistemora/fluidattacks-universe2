/* eslint-disable react/forbid-component-props
  --------
  We need className to override default styles in
  order to pass down props to react-bootstrap Button.
*/
import { Button } from "react-bootstrap";
import FontAwesome from "react-fontawesome";
import React from "react";

interface ILoginButtonProps {
  bsStyle: string;
  className: string;
  fontAwesomeName: string;
  onClick: () => void;
  text: string;
}

const loginButton: React.FC<ILoginButtonProps> = (
  props: Readonly<ILoginButtonProps>
): JSX.Element => {
  const { bsStyle, className, fontAwesomeName, onClick, text } = props;

  return (
    <Button
      block={true}
      bsStyle={bsStyle}
      className={className}
      onClick={onClick}
    >
      <FontAwesome name={fontAwesomeName} size={"2x"} />
      {text}
    </Button>
  );
};

export { loginButton as LoginButton };
