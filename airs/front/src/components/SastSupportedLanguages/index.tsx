/* eslint react/forbid-component-props: 0 */
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { BlackH2 } from "../../styles/styledComponents";

const LanguagesListContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    mw-1366
    ph-body
    center
    pv5
    v-top
    mb5
  `,
})``;
const ListContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    center 
    moon-gray 
    mw8
  `,
})``;
const ListColumn: StyledComponent<
  "ul",
  Record<string, unknown>
> = styled.ul.attrs({
  className: `
    list
    roboto
    f3-ns
    f4
    fw7
    dib-l
    ph4
    mv0
    pv0-l
    pv4
    tl
  `,
})``;

export const LanguagesList: React.FC = (): JSX.Element => (
  <LanguagesListContainer>
    <BlackH2 className={"roboto"}>{"Supported Languages"}</BlackH2>
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
