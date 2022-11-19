/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React, { useState } from "react";
import { FaMinus, FaPlus } from "react-icons/fa";

import { Button } from "../../../../components/Button";
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
    <Container borderBottom={"1px"}>
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
          <Button
            icon={icon === "plus" ? <FaPlus /> : <FaMinus />}
            onClick={showDescription}
          />
        </Container>
      </Container>
      <Container
        display={description === "none" ? "none" : "flex"}
        justify={"start"}
      >
        {children}
      </Container>
    </Container>
  );
};

export { SolutionFaq };
