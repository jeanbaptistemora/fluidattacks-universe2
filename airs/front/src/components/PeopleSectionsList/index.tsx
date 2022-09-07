/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";

import { PeopleSection } from "./Section";

import { translate } from "../../utils/translations/translate";

const PeopleSectionList: React.FC = (): JSX.Element => (
  <div className={"w-100"}>
    <PeopleSection
      description={translate.t("people.fluidAttacks.description")}
      imageAlt={"Fluid Attacks Team"}
      imageSide={"left"}
      imageSrc={"/airs/about-us/people/people-1_nvmjti"}
      title={translate.t("people.fluidAttacks.title")}
    />
    <PeopleSection
      description={translate.t("people.hackingTeam.description")}
      imageAlt={"Hacking Team"}
      imageSide={"right"}
      imageSrc={"/airs/about-us/people/people-2_gys0ia"}
      title={translate.t("people.hackingTeam.title")}
    />
    <PeopleSection
      description={translate.t("people.product.description")}
      imageAlt={"Product & Projects Teams"}
      imageSide={"left"}
      imageSrc={"/airs/about-us/people/people-3_nftkzj"}
      title={translate.t("people.product.title")}
    />
    <PeopleSection
      description={translate.t("people.marketing.description")}
      imageAlt={"Marketing & Sales Teams"}
      imageSide={"right"}
      imageSrc={"/airs/about-us/people/people-4_fqwtae.png"}
      title={translate.t("people.marketing.title")}
    />
  </div>
);

export { PeopleSectionList };
