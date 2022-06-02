import styled from "styled-components";

import { Tab } from "./Tab";

const Tabs = styled.ul.attrs({
  className: "flex justify-around list ma0",
})`
  background-color: #f4f4f6;
  padding: 12px 0;
`;

export { Tab, Tabs };
