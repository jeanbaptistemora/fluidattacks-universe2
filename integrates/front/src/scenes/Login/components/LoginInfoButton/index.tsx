import FontAwesome from "react-fontawesome";
import React from "react";

interface ILoginInfoButtonProps {
  fontAwesomeName: string;
  className: string;
  onClick: () => void;
}

const loginInfoButton: React.FC<ILoginInfoButtonProps> = (
  props: Readonly<ILoginInfoButtonProps>
): JSX.Element => {
  const { fontAwesomeName, className, onClick } = props;

  return (
    <button className={className} onClick={onClick}>
      <FontAwesome name={fontAwesomeName} size={"2x"} />
      &nbsp;
    </button>
  );
};

export { loginInfoButton as LoginInfoButton };
