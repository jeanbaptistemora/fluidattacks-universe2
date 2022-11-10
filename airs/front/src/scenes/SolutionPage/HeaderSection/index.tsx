/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";

import { AirsLink } from "../../../components/AirsLink";
import { Button } from "../../../components/Button";
import { Container } from "../../../components/Container";
import { Text, Title } from "../../../components/Typography";

interface IHeaderProps {
  description: string;
  title: string;
}

const HeaderSection: React.FC<IHeaderProps> = ({
  description,
  title,
}): JSX.Element => {
  return (
    <Container bgColor={"#f4f4f6"} ph={4} pv={5}>
      <Container center={true} maxWidth={"1200px"}>
        <Title
          color={"2e2e38"}
          level={1}
          mb={3}
          size={"big"}
          textAlign={"center"}
        >
          {title}
        </Title>
        <Text color={"#535365"} size={"medium"} textAlign={"center"}>
          {description}
        </Text>
        <Container display={"flex"} justify={"center"} mt={3} wrap={"wrap"}>
          <Container ph={1} pv={1} width={"auto"} widthSm={"100%"}>
            <AirsLink href={"/free-trial/"}>
              <Button display={"block"} variant={"primary"}>
                {"Start free trial"}
              </Button>
            </AirsLink>
          </Container>
          <Container ph={1} pv={1} width={"auto"} widthSm={"100%"}>
            <AirsLink href={"/contact-us/"}>
              <Button display={"block"} variant={"tertiary"}>
                {"Contact now"}
              </Button>
            </AirsLink>
          </Container>
        </Container>
      </Container>
    </Container>
  );
};

export { HeaderSection };
