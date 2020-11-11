/* eslint-disable react/forbid-component-props
  --------
  We need className to override default styles in
  order to pass down props to react-bootstrap Button.
*/
import FontAwesome from "react-fontawesome";
import React from "react";

interface ILoginButtonProps {
  className: string;
  fontAwesomeName: string;
  onClick: () => void;
  text: string;
}

const loginButton: React.FC<ILoginButtonProps> = (
  props: Readonly<ILoginButtonProps>
): JSX.Element => {
  const { className, fontAwesomeName, onClick, text } = props;

  return (
    <button className={className + " pa3 dim"} onClick={onClick}>
      <FontAwesome name={fontAwesomeName} size={"2x"} />
      {text}
    </button>
  );
};

export { loginButton as LoginButton };
