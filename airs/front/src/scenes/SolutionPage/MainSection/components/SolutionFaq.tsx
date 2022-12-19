import React, { useState } from "react";
import { FaMinus, FaPlus } from "react-icons/fa";

import { Container } from "../../../../components/Container";
import { Title } from "../../../../components/Typography";

interface IFaqProps {
  title: string;
}

const SolutionFaq: React.FC<IFaqProps> = ({ children, title }): JSX.Element => {
  const [description, setDescription] = useState("none");
  const [icon, setIcon] = useState("plus");
  function showDescription(): void {
    if (description === "none") {
      setDescription("block");
    } else {
      setDescription("none");
    }
    if (icon === "plus") {
      setIcon("minus");
    } else {
      setIcon("plus");
    }
  }

  return (
    <Container borderBottomColor={"#dddde3"} onClick={showDescription}>
      <Container
        align={"center"}
        display={"flex"}
        justify={"between"}
        maxWidth={"1200px"}
        pv={3}
        width={"100%"}
        wrap={"wrap"}
      >
        <Container width={"80%"}>
          <Title color={"#2e2e38"} level={3} size={"xs"}>
            {title}
          </Title>
        </Container>
        <Container display={"flex"} justify={"end"} mr={0} width={"20%"}>
          {icon === "plus" ? <FaPlus /> : <FaMinus />}
        </Container>
      </Container>
      <Container
        display={description === "none" ? "none" : "block"}
        justify={"start"}
      >
        {children}
      </Container>
    </Container>
  );
};

export { SolutionFaq };
