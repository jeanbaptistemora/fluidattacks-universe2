import React from "react";

import { Container } from "../../../../components/Container";

interface IQuoteProps {
  children: React.ReactNode;
}

const Quote: React.FC<IQuoteProps> = ({ children }): JSX.Element => (
  <Container bgColor={"#F4F4F6"} borderColor={"#8F8FA3"} br={3} mv={3} ph={3}>
    {children}
  </Container>
);

export { Quote };
