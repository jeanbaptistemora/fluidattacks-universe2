/* eslint import/no-unresolved:0 */
/* eslint @typescript-eslint/no-magic-numbers:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint fp/no-mutation:0 */
/* eslint import/no-namespace:0 */
/* eslint react/jsx-no-bind:0 */
import { faAngleLeft, faAngleRight } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useEffect, useState } from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import logoAvianca from "../../../../static/images/about-us/clients/logo-avianca.png";
import logoBancoGeneral from "../../../../static/images/about-us/clients/logo-banco-general.png";
import logoBancoIndustrial from "../../../../static/images/about-us/clients/logo-banco-industrial.png";
import logoBancolombia from "../../../../static/images/about-us/clients/logo-bancolombia.png";
import logoBanesco from "../../../../static/images/about-us/clients/logo-banesco.png";
import logoBanistmo from "../../../../static/images/about-us/clients/logo-banistmo.png";
import logoBantrab from "../../../../static/images/about-us/clients/logo-bantrab.png";
import logoColmedica from "../../../../static/images/about-us/clients/logo-colmedica.png";
import logoInterbank from "../../../../static/images/about-us/clients/logo-interbank.png";
import logoItau from "../../../../static/images/about-us/clients/logo-itau.png";
import logoOxxo from "../../../../static/images/about-us/clients/logo-oxxo.png";
import logoSodimac from "../../../../static/images/about-us/clients/logo-sodimac.png";
import logoSura from "../../../../static/images/about-us/clients/logo-sura.png";
import {
  BannerContainer,
  FontAwesomeContainerSmall,
} from "../../../styles/styledComponents";
import { translate } from "../../../utils/translations/translate";

const Container: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    h-500
    mw-1366
    center
    flex-l
    mb1-l
    mb6
  `,
})``;

const ClientsTitle: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    neue
    f3
    tl
    fw7
    c-fluid-bk
    pv4
    ph-body
  `,
})``;

const ArrowButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    bg-fluid-gray
    bn
    pa3
    dib
    pointer
    outline-transparent
  `,
})``;

const SlideShow: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-100
    slide-show
    overflow-hidden-l
    overflow-x-auto
    t-all-3-eio
    scroll-smooth
    nowrap
    mw-376
    center
    br-l
    b--light-gray
  `,
})``;

const ArrowContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    bt
    b--light-gray
    tr
  `,
})``;

const DefinitionContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    pa6-l
    ph-body
  `,
})``;

const DefinitionParagraph: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    roboto
    c-black-gray
    fw4
    f5
    lh-copy
    mv4
  `,
})``;

const ClientsSection: React.FC = (): JSX.Element => {
  const [scroll, setScroll] = useState(0);

  const scrollLeft: () => void = (): void => {
    setScroll(scroll < 376 ? 0 : scroll - 376);
  };

  const scrollRight: () => void = (): void => {
    setScroll(scroll > 4136 ? 4512 : scroll + 376);
  };

  const changeScroll: (element: HTMLElement) => void = (
    element: HTMLElement
  ): void => {
    if (element.scrollLeft > 0 || element.scrollLeft < 4512) {
      element.scrollLeft = scroll;
    } else {
      element.scrollLeft += 0;
    }
  };

  useEffect((): void => {
    const slideShow: HTMLElement = document.getElementById(
      "clientsSlides"
    ) as HTMLElement;
    changeScroll(slideShow);
  });

  return (
    <React.Fragment>
      <BannerContainer className={"bg-clients-home"} />
      <Container>
        <div>
          <ClientsTitle>{translate.t("clients.titleHome")}</ClientsTitle>
          <ArrowContainer>
            <ArrowButton onClick={scrollLeft}>
              <FontAwesomeContainerSmall>
                <FontAwesomeIcon
                  className={"f3 c-black-gray"}
                  icon={faAngleLeft}
                />
              </FontAwesomeContainerSmall>
            </ArrowButton>
            <ArrowButton onClick={scrollRight}>
              <FontAwesomeContainerSmall>
                <FontAwesomeIcon
                  className={"f3 c-black-gray"}
                  icon={faAngleRight}
                />
              </FontAwesomeContainerSmall>
            </ArrowButton>
          </ArrowContainer>
          <SlideShow id={"clientsSlides"}>
            <img alt={"Logo Avianca"} className={"mh4"} src={logoAvianca} />
            <img
              alt={"Logo Banco General"}
              className={"mh4"}
              src={logoBancoGeneral}
            />
            <img
              alt={"Logo Banco Industrial"}
              className={"mh4"}
              src={logoBancoIndustrial}
            />
            <img
              alt={"Logo Bancolombia"}
              className={"mh4"}
              src={logoBancolombia}
            />
            <img alt={"Logo Banesco"} src={logoBanesco} />
            <img alt={"Logo Banistmo"} className={"mh4"} src={logoBanistmo} />
            <img alt={"Logo Bantrab"} src={logoBantrab} />
            <img alt={"Logo Colmedica"} className={"mh4"} src={logoColmedica} />
            <img alt={"Logo Interbank"} className={"mh4"} src={logoInterbank} />
            <img alt={"Logo Itau"} className={"mh4"} src={logoItau} />
            <img alt={"Logo Oxxo"} src={logoOxxo} />
            <img alt={"Logo Sodimac"} src={logoSodimac} />
            <img alt={"Logo Sura"} className={"mh4"} src={logoSura} />
          </SlideShow>
        </div>
        <DefinitionContainer>
          <DefinitionParagraph>
            {translate.t("clients.definition")}
          </DefinitionParagraph>
        </DefinitionContainer>
      </Container>
    </React.Fragment>
  );
};

export { ClientsSection };
