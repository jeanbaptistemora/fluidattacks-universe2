import styled from "styled-components";

import { CardBody } from "./Body";
import { CardHeader } from "./Header";

const Card = styled.article.attrs({ className: "ba br2 pa3" })`
  background-color: #f4f4f6;
  border-color: transparent;
  border-width: 2px;
  box-shadow: 0px 0px 8px 1px rgb(0 0 0 / 10%);
  transition: all 0.2s ease-in;

  :hover {
    border-color: #ff3435;
  }
`;

export { Card, CardBody, CardHeader };
