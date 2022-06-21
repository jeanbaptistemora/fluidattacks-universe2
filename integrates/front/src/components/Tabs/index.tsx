import styled from "styled-components";

import { Tab } from "./Tab";

const Tabs = styled.ul.attrs({
  className: "flex justify-around list ma0",
})`
  background-color: #f4f4f6;
  border: 1px solid #d2d2da;
  border-radius: 4px;
  padding: 0;
`;

export { Tab, Tabs };
