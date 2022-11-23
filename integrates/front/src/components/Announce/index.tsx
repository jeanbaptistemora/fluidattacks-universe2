import React from "react";

import { Container } from "./styles";

import { Logo } from "components/Logo";

interface IAnnounceProps {
  message: string;
}

const Announce: React.FC<IAnnounceProps> = ({
  message,
}: IAnnounceProps): JSX.Element => {
  return (
    <Container>
      <Logo height={50} width={50} />
      <p>{message}</p>
    </Container>
  );
};

export type { IAnnounceProps };
export { Announce };
