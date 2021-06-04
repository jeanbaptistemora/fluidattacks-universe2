/* eslint import/no-unresolved:0 */
/* eslint @typescript-eslint/no-magic-numbers:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint fp/no-mutation:0 */
/* eslint react/jsx-no-bind:0 */
import { faAngleLeft, faAngleRight } from "@fortawesome/pro-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useEffect, useState } from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import {
  BannerContainer,
  FontAwesomeContainerSmall,
} from "../../../styles/styledComponents";
import { translate } from "../../../utils/translations/translate";
import { CloudImage } from "../../CloudImage";

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

const ClientsContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    br
    b--light-gray
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
    mw-446
    center
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
    ph-body
    flex
    justify-center
    items-center
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
    mw7-l
    mw6
  `,
})``;

const ClientsSection: React.FC = (): JSX.Element => {
  const [scroll, setScroll] = useState(0);

  const scrollLeft: () => void = (): void => {
    setScroll(scroll < 446 ? 0 : scroll - 446);
  };

  const scrollRight: () => void = (): void => {
    setScroll(scroll > 12488 ? 12934 : scroll + 446);
  };

  const changeScroll: (element: HTMLElement) => void = (
    element: HTMLElement
  ): void => {
    if (element.scrollLeft > 0 || element.scrollLeft < 12934) {
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
      <BannerContainer className={"bg-clients-home bg-attachment-fixed"} />
      <Container>
        <ClientsContainer className={"bg-lightgray nt6"}>
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
            <CloudImage
              alt={"Logo Abbott"}
              src={"airs/clients/logo-abbott"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Addi"}
              src={"airs/clients/logo-addi"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Avianca"}
              src={"airs/clients/logo-avianca"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Axxa Colpatria"}
              src={"airs/clients/logo-axxa-colpatria"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Banco Azul"}
              src={"airs/clients/logo-banco-azul"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Banco General"}
              src={"airs/clients/logo-banco-general"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Banco Industrial"}
              src={"airs/clients/logo-banco-industrial"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Banco Pichincha"}
              src={"airs/clients/logo-banco-pichincha"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Bancolombia"}
              src={"airs/clients/logo-bancolombia"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Banesco"}
              src={"airs/clients/logo-banesco"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Banistmo"}
              src={"airs/clients/logo-banistmo"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Bantrab"}
              src={"airs/clients/logo-bantrab"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Banco Bisa"}
              src={"airs/clients/logo-bisa"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Btg Pactual"}
              src={"airs/clients/logo-btg"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Colmedica"}
              src={"airs/clients/logo-colmedica"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Global Bank"}
              src={"airs/clients/logo-global-bank"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Interbank"}
              src={"airs/clients/logo-interbank"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Itau"}
              src={"airs/clients/logo-itau"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Libera"}
              src={"airs/clients/logo-libera"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Manpower"}
              src={"airs/clients/logo-manpower"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Mazda"}
              src={"airs/clients/logo-mazda"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Oxxo"}
              src={"airs/clients/logo-oxxo"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Payvalida"}
              src={"airs/clients/logo-payvalida"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Quipux"}
              src={"airs/clients/logo-quipux"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Redeban"}
              src={"airs/clients/logo-redeban"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Rsa"}
              src={"airs/clients/logo-rsa"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Sodimac"}
              src={"airs/clients/logo-sodimac"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Soy yo"}
              src={"airs/clients/logo-soy-yo"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Sura"}
              src={"airs/clients/logo-sura"}
              styles={"mh4"}
            />
            <CloudImage
              alt={"Logo Terpel"}
              src={"airs/clients/logo-terpel"}
              styles={"mh4"}
            />
          </SlideShow>
        </ClientsContainer>
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
