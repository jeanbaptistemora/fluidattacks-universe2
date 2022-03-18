import styled from "styled-components";

import { TimelineItem } from "./Item";

const Timeline = styled.ol.attrs({
  className: "flex flex-column list pa0 relative",
})`
  li:nth-child(odd) {
    align-self: flex-start;
    justify-content: flex-end;
  }

  li:nth-child(even) {
    align-self: flex-end;
    justify-content: flex-start;
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
