/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint import/no-unresolved:0 */
/* eslint @typescript-eslint/no-magic-numbers:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint fp/no-mutation:0 */
/* eslint react/jsx-no-bind:0 */
import React from "react";

import { ClientsContainer, Container, SlideShow } from "./styledComponents";

import { translate } from "../../../utils/translations/translate";
import { CloudImage } from "../../CloudImage";
import { Title } from "../../Texts";

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
        {translate.t("clients.newTitleHome")}
      </Title>
      <ClientsContainer gradientColor={sectionColor}>
        <SlideShow>
          <CloudImage
            alt={"Logo Abbott"}
            src={"airs/clients-carousel/logo-abbott"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Addi"}
            src={"airs/clients-carousel/logo-addi"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Avianca"}
            src={"airs/clients-carousel/logo-avianca"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Banco Azul"}
            src={"airs/clients-carousel/logo-banco-azul"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Banco General"}
            src={"airs/clients-carousel/logo-banco-general"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Banco Industrial"}
            src={"airs/clients-carousel/logo-banco-industrial"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Banco Pichincha"}
            src={"airs/clients-carousel/logo-banco-pichincha"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Bancolombia"}
            src={"airs/clients-carousel/logo-bancolombia"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Banesco"}
            src={"airs/clients-carousel/logo-banesco"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Banistmo"}
            src={"airs/clients-carousel/logo-banistmo"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Bantrab"}
            src={"airs/clients-carousel/logo-bantrab"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Banco Bisa"}
            src={"airs/clients-carousel/logo-bisa"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Btg Pactual"}
            src={"airs/clients-carousel/logo-btg"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Colmedica"}
            src={"airs/clients-carousel/logo-colmedica"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Global Bank"}
            src={"airs/clients-carousel/logo-global-bank"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Interbank"}
            src={"airs/clients-carousel/logo-interbank"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Itau"}
            src={"airs/clients-carousel/logo-itau"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Libera"}
            src={"airs/clients-carousel/logo-libera"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Mazda"}
            src={"airs/clients-carousel/logo-mazda"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Oxxo"}
            src={"airs/clients-carousel/logo-oxxo"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Payvalida"}
            src={"airs/clients-carousel/logo-payvalida"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Quipux"}
            src={"airs/clients-carousel/logo-quipux"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Redeban"}
            src={"airs/clients-carousel/logo-redeban"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Rsa"}
            src={"airs/clients-carousel/logo-rsa"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Sodimac"}
            src={"airs/clients-carousel/logo-sodimac"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Soy yo"}
            src={"airs/clients-carousel/logo-soy-yo"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Sura"}
            src={"airs/clients-carousel/logo-sura"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Terpel"}
            src={"airs/clients-carousel/logo-terpel"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Abbott"}
            src={"airs/clients-carousel/logo-abbott"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Addi"}
            src={"airs/clients-carousel/logo-addi"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Avianca"}
            src={"airs/clients-carousel/logo-avianca"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Banco Azul"}
            src={"airs/clients-carousel/logo-banco-azul"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Banco General"}
            src={"airs/clients-carousel/logo-banco-general"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Banco Industrial"}
            src={"airs/clients-carousel/logo-banco-industrial"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Banco Pichincha"}
            src={"airs/clients-carousel/logo-banco-pichincha"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Bancolombia"}
            src={"airs/clients-carousel/logo-bancolombia"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Banesco"}
            src={"airs/clients-carousel/logo-banesco"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Banistmo"}
            src={"airs/clients-carousel/logo-banistmo"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Bantrab"}
            src={"airs/clients-carousel/logo-bantrab"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Banco Bisa"}
            src={"airs/clients-carousel/logo-bisa"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Btg Pactual"}
            src={"airs/clients-carousel/logo-btg"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Colmedica"}
            src={"airs/clients-carousel/logo-colmedica"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Global Bank"}
            src={"airs/clients-carousel/logo-global-bank"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Interbank"}
            src={"airs/clients-carousel/logo-interbank"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Itau"}
            src={"airs/clients-carousel/logo-itau"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Libera"}
            src={"airs/clients-carousel/logo-libera"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Mazda"}
            src={"airs/clients-carousel/logo-mazda"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Oxxo"}
            src={"airs/clients-carousel/logo-oxxo"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Payvalida"}
            src={"airs/clients-carousel/logo-payvalida"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Quipux"}
            src={"airs/clients-carousel/logo-quipux"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Redeban"}
            src={"airs/clients-carousel/logo-redeban"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Rsa"}
            src={"airs/clients-carousel/logo-rsa"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Sodimac"}
            src={"airs/clients-carousel/logo-sodimac"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Soy yo"}
            src={"airs/clients-carousel/logo-soy-yo"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Sura"}
            src={"airs/clients-carousel/logo-sura"}
            styles={"mh4"}
          />
          <CloudImage
            alt={"Logo Terpel"}
            src={"airs/clients-carousel/logo-terpel"}
            styles={"mh4"}
          />
        </SlideShow>
      </ClientsContainer>
    </Container>
  );
};

export { ClientsSection };
