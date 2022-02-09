/* eslint import/no-unresolved:0 */
/* eslint @typescript-eslint/no-magic-numbers:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint fp/no-mutation:0 */
/* eslint react/jsx-no-bind:0 */
import React from "react";

import {
  ClientsContainer,
  Container,
  SlideShow,
  TitleContainer,
} from "./styledComponents";

import { WhiteBigParagraph } from "../../../styles/styledComponents";
import { translate } from "../../../utils/translations/translate";
import { CloudImage } from "../../CloudImage";

const ClientsSection: React.FC = (): JSX.Element => {
  return (
    <Container>
      <TitleContainer>
        <WhiteBigParagraph>
          {translate.t("clients.newTitleHome")}
        </WhiteBigParagraph>
      </TitleContainer>
      <ClientsContainer>
        <SlideShow>
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
    </Container>
  );
};

export { ClientsSection };
