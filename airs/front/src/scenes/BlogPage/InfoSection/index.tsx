import React from "react";

import type { IInfoProps } from "./types";

import { AirsLink } from "../../../components/AirsLink";
import { CloudImage } from "../../../components/CloudImage";
import { Container } from "../../../components/Container";
import { Text } from "../../../components/Typography";
import { stringToUri } from "../../../utils/utilities";

const InfoSection: React.FC<IInfoProps> = ({
  author,
  date,
  writer,
}): JSX.Element => {
  return (
    <Container bgColor={"#fff"} ph={4}>
      <Container
        align={"center"}
        borderBottomColor={"#bf0b1a"}
        center={true}
        display={"flex"}
        maxWidth={"1440px"}
        pv={3}
      >
        <Container align={"center"} display={"flex"}>
          <Container height={"54px"} mr={3} width={"54px"}>
            <CloudImage
              alt={writer}
              src={`airs/blogs/authors/${writer}`}
              styles={"w-100 h-100"}
            />
          </Container>
          <AirsLink
            decoration={"underline"}
            hoverColor={"#bf0b1a"}
            href={`/blog/authors/${stringToUri(author)}`}
          >
            <Text color={"#2e2e38"} sizeSm={"xs"}>
              {author}
            </Text>
          </AirsLink>
        </Container>
        <Container>
          <Text color={"#2e2e38"} sizeSm={"xs"} textAlign={"end"}>
            {date}
          </Text>
        </Container>
      </Container>
    </Container>
  );
};

export { InfoSection };
