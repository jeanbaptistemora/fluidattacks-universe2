import React from "react";

import { Container } from "components/Container";
import { starMedium, starSolid } from "resources";

export const StarsMedium: React.FC = (): JSX.Element => {
  return (
    <Container display={"flex"} pb={"24px"} wrap={"wrap"}>
      {[...Array(4).keys()].map(
        (el: number): JSX.Element => (
          <Container
            bgImage={`url(${starSolid})`}
            bgImagePos={"100% 100%"}
            height={"20px"}
            key={el}
            margin={"0px 16px 0px 0px"}
            width={"21px"}
          />
        )
      )}
      <Container
        bgImage={`url(${starMedium})`}
        bgImagePos={"100% 100%"}
        height={"20px"}
        margin={"0px 16px 0px 0px"}
        width={"21px"}
      />
    </Container>
  );
};
