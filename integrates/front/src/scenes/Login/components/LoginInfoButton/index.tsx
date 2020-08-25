import { Button } from "react-bootstrap";
import FontAwesome from "react-fontawesome";
import React from "react";

interface ILoginInfoButtonProps {
  bsStyle: string;
  fontAwesomeName: string;
  href: string;
}

const loginInfoButton: React.FC<ILoginInfoButtonProps> = (
  props: Readonly<ILoginInfoButtonProps>
): JSX.Element => {
  const { bsStyle, fontAwesomeName, href } = props;

  return (
    <Button block={true} bsStyle={bsStyle} href={href}>
      <FontAwesome name={fontAwesomeName} size={"2x"} />
      &nbsp;
    </Button>
  );
};

export { loginInfoButton as LoginInfoButton };
