import React from "react";

import { ClientsContainer, Container, SlideShow } from "./styledComponents";

import { CloudImage } from "../../../components/CloudImage";
import { Title } from "../../../components/Texts";
import { translate } from "../../../utils/translations/translate";

interface IClientsSectionProps {
  sectionColor: string;
  titleColor: string;
  titleSize: string;
}

const ClientsSection: React.FC<IClientsSectionProps> = ({
  sectionColor,
  titleColor,
  titleSize,
}: IClientsSectionProps): JSX.Element => {
  return (
    <Container bgColor={sectionColor}>
      <Title fColor={titleColor} fSize={titleSize} marginBottom={"4"}>
        {translate.t("home.clients.title")}
      </Title>
      <ClientsContainer gradientColor={sectionColor}>
        <SlideShow>
          {[...Array(48).keys()].map(
            (el: number): JSX.Element =>
              el === 0 ? (
                <div key={el} />
              ) : (
                <CloudImage
                  alt={`logo-gray(${el})`}
                  key={`logo-gray(${el})`}
                  src={`airs/home/ClientSection/logos-gray_${el}.png`}
                  styles={"mh3"}
                />
              )
          )}
        </SlideShow>
      </ClientsContainer>
    </Container>
  );
};

export { ClientsSection };
