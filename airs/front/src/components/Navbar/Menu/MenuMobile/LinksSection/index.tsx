/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint import/no-unresolved:0 */
import React from "react";

import { MenuLinksContainer } from "../../../../../styles/styledComponents";
import { MenuLink } from "../MenuLink";

const LinksSection: React.FC = (): JSX.Element => (
  <MenuLinksContainer>
    <div className={"mr3 mb3"}>
      <MenuLink link={"/plans/"} name={"Plans"} />
      <MenuLink link={"/certifications/"} name={"Certifications"} />
      <MenuLink link={"/blog/"} name={"Blog"} />
      <MenuLink link={"/partners/"} name={"Partners"} />
    </div>
    <div>
      <MenuLink link={"/careers/"} name={"Careers"} />
      <MenuLink link={"/advisories/"} name={"Advisories"} />
      <MenuLink link={"/faq/"} name={"FAQ"} />
      <MenuLink
        link={"https://docs.fluidattacks.com/"}
        name={"Documentation"}
      />
    </div>
  </MenuLinksContainer>
);

export { LinksSection };
