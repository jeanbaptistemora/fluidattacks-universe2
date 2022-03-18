import styled from "styled-components";

import { TimelineItem } from "./Item";

const Timeline = styled.ol.attrs({
  className: "flex flex-column list pa0 relative",
})`
  li:nth-child(odd) {
    align-self: flex-start;
    justify-content: flex-end;
  }

  li:nth-child(odd) article::after {
    right: -16px;
  }

  li:nth-child(odd) article::before {
    border-color: transparent transparent transparent white;
    border-width: 10px 0 10px 10px;
    right: 30px;
  }

  li:nth-child(even) {
    align-self: flex-end;
    justify-content: flex-start;
  }

  li:nth-child(even) article::after {
    left: -16px;
  }

  li:nth-child(even) article::before {
    border-color: transparent white transparent transparent;
    border-width: 10px 10px 10px 0;
    left: 30px;
  }

  ::after {
    background-color: white;
    content: "";
    height: 100%;
    left: calc(50% - 3px);
    position: absolute;
    width: 6px;
  }
`;

export { Timeline, TimelineItem };
