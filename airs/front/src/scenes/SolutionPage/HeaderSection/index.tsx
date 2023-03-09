/* eslint react/jsx-no-bind:0 */
import { useMatomo } from "@datapunt/matomo-tracker-react";
import React, { useCallback } from "react";

import { AirsLink } from "../../../components/AirsLink";
import { Button } from "../../../components/Button";
import { Container } from "../../../components/Container";
import { Text, Title } from "../../../components/Typography";

interface IHeaderProps {
  description: string;
  image: string;
  title: string;
}

const HeaderSection: React.FC<IHeaderProps> = ({
  description,
  image,
  title,
}): JSX.Element => {
  const { trackEvent } = useMatomo();

  const matomoFreeTrialEvent = useCallback((): void => {
    trackEvent({
      action: "header-free-trial-click",
      category: "solution",
    });
  }, [trackEvent]);

  return (
    <Container bgColor={"#f4f4f6"} ph={4} pv={5}>
      <Container center={true} maxWidth={"1200px"}>
        <Title
          color={"#2e2e38"}
          level={1}
          mb={3}
          size={"big"}
          sizeSm={"medium"}
          textAlign={"center"}
        >
          {title}
        </Title>
        <Text color={"#535365"} size={"medium"} textAlign={"center"}>
          {description}
        </Text>
        <Container display={"flex"} justify={"center"} mv={3} wrap={"wrap"}>
          <Container pv={1} width={"auto"} widthSm={"100%"}>
            <AirsLink
              decoration={"none"}
              href={"https://app.fluidattacks.com/SignUp"}
            >
              <Button
                display={"block"}
                onClick={matomoFreeTrialEvent}
                variant={"primary"}
              >
                {"Start free trial"}
              </Button>
            </AirsLink>
          </Container>
          <Container ph={3} phSm={0} pv={1} width={"auto"} widthSm={"100%"}>
            <AirsLink href={"/contact-us/"}>
              <Button display={"block"} variant={"tertiary"}>
                {"Contact now"}
              </Button>
            </AirsLink>
          </Container>
        </Container>
        <Container center={true} width={"950px"} widthSm={"100%"}>
          <img
            alt={`solution ${title}`}
            className={"w-100 h-100"}
            src={image}
          />
        </Container>
      </Container>
    </Container>
  );
};

export { HeaderSection };
