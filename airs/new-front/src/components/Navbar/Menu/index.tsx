/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
import { MenuButton } from "../../../styles/styledComponents";
import React from "react";

const Menu: React.FC = (): JSX.Element => (
  <MenuButton>
    <div className={"lower"}>
      <span className={"pointer dib h2-l"} id={"openbtn"}>
        <img
          alt={"Menu open icon"}
          className={"w2"}
          src={"https://fluidattacks.com/theme/images/menu.svg"}
        />
      </span>
    </div>
  </MenuButton>
);

export { Menu };
