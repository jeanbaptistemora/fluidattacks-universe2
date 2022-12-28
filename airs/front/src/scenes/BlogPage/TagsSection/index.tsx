import React from "react";

import { AirsLink } from "../../../components/AirsLink";
import { Button } from "../../../components/Button";
import { Container } from "../../../components/Container";
import { Text } from "../../../components/Typography";
import { capitalizeDashedString } from "../../../utils/utilities";

interface ITagsProps {
  tags: string;
}

const TagsSection: React.FC<ITagsProps> = ({ tags }): JSX.Element => {
  const tagsList = tags.split(", ").flat();

  return (
    <Container ph={4}>
      <Container
        borderTopColor={"#b0b0bf"}
        center={true}
        maxWidth={"1440px"}
        pv={3}
      >
        <Text
          color={"#2e2e38"}
          display={"inline-block"}
          mr={1}
          size={"big"}
          weight={"bold"}
        >
          {"Tags:"}
        </Text>
        {tagsList.map((tag): JSX.Element => {
          return (
            <AirsLink href={`/blog/tags/${tag}`} key={tag}>
              <Button>{capitalizeDashedString(tag)}</Button>
            </AirsLink>
          );
        })}
      </Container>
    </Container>
  );
};

export { TagsSection };
