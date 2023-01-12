import React from "react";

import { Container } from "../../../../components/Container";

interface ICautionProps {
  children: React.ReactNode;
}

const Caution: React.FC<ICautionProps> = ({ children }): JSX.Element => (
  <Container bgColor={"#FFECED"} borderColor={"#BF0B1A"} br={3} mv={3} ph={3}>
    {children}
  </Container>
);

export { Caution };
