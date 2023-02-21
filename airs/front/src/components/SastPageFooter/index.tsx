/* eslint react/forbid-component-props: 0 */
import React from "react";

import {
  LanguagesListContainer,
  ListColumn,
  ListContainer,
  SastParagraph,
} from "./styledComponents";

import { translate } from "../../utils/translations/translate";
import { CloudImage } from "../CloudImage";
import { Title } from "../Texts";

export const SastPageFooter: React.FC = (): JSX.Element => (
  <LanguagesListContainer>
    <SastParagraph>
      <CloudImage
        alt={"OWASP-logo"}
        src={"/airs/product/icon-logo-owasp-rojo"}
        styles={"pr3 w3 h3"}
      />
      <p className={"ma0"}>{translate.t("sastCategoryParagraph.phrase1")}</p>
      <b className={"ma0"}>{translate.t("sastCategoryParagraph.bold1")}</b>
      <Title fColor={"#2e2e38"} fSize={"24"} marginTop={"4"}>
        {"Supported Languages"}
      </Title>
    </SastParagraph>
    <ListContainer>
      <ListColumn>
        <li>{"ABAP"}</li>
        <li>{"ActionScript"}</li>
        <li>{"ASP.NET"}</li>
        <li>{"Apex"}</li>
        <li>{"C"}</li>
        <li>{"C#"}</li>
        <li>{"C++"}</li>
        <li>{"Cloudformation"}</li>
        <li>{"Cobol"}</li>
        <li>{"Go"}</li>
      </ListColumn>
      <ListColumn>
        <li>{"Hana SQL Script"}</li>
        <li>{"HTML"}</li>
        <li>{"Informix"}</li>
        <li>{"Java"}</li>
        <li>{"JavaScript/TypeScript"}</li>
        <li>{"JCL"}</li>
        <li>{"JSP"}</li>
        <li>{"Kotlin"}</li>
        <li>{"Natural"}</li>
        <li>{"Objective C"}</li>
      </ListColumn>
      <ListColumn>
        <li>{"OracleForms"}</li>
        <li>{"PHP"}</li>
        <li>{"PL-SQL"}</li>
        <li>{"PL1"}</li>
        <li>{"PowerScript"}</li>
        <li>{"Python"}</li>
        <li>{"RPG4"}</li>
        <li>{"Ruby"}</li>
        <li>{"Scala"}</li>
        <li>{"SQL"}</li>
      </ListColumn>
      <ListColumn className={"v-top"}>
        <li>{"SQL"}</li>
        <li>{"Swift"}</li>
        <li>{"TAL"}</li>
        <li>{"Terraform"}</li>
        <li>{"Transact-SQL"}</li>
        <li>{"VB.NET"}</li>
        <li>{"VisualBasic 6"}</li>
        <li>{"XML"}</li>
      </ListColumn>
    </ListContainer>
  </LanguagesListContainer>
);
