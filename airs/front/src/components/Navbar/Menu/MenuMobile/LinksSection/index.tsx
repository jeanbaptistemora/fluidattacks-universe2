/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint import/no-unresolved:0 */
import React from "react";

import { MenuLinksContainer } from "../../../../../styles/styledComponents";
import { MenuLink } from "../MenuLink";

const LinksSection: React.FC = (): JSX.Element => (
  <MenuLinksContainer>
    <div className={"mr3"}>
      <MenuLink link={"/blog/"} name={"Blog"} />
      <MenuLink link={"/partners/"} name={"Partners"} />
      <MenuLink link={"/advisories/"} name={"Advisories"} />
    </div>
    <div>
      <MenuLink link={"/careers/"} name={"Careers"} />
      <MenuLink link={"/faq/"} name={"FAQ"} />
      <MenuLink link={"/plans/"} name={"Plans"} />
    </div>
  </MenuLinksContainer>
);

export { LinksSection };
