import styled from "styled-components";

import { TimelineItem } from "./Item";

const Timeline = styled.ol.attrs({
  className: "flex flex-column list pa0 relative",
})`
  li:nth-child(odd) {
    align-self: flex-start;
    justify-content: flex-end;
  }

  li:nth-child(odd)::after {
    right: -16px;
  }

  li:nth-child(odd)::before {
    border-color: transparent transparent transparent white;
    border-width: 10px 0 10px 10px;
    right: 31px;
  }

  li:nth-child(even) {
    align-self: flex-end;
    justify-content: flex-start;
  }

  li:nth-child(even)::after {
    left: -16px;
  }

  li:nth-child(even)::before {
    border-color: transparent white transparent transparent;
    border-width: 10px 10px 10px 0;
    left: 31px;
  }

  ::after {
    background-color: white;
    content: "";
    height: 100%;
    left: calc(50% - 3px);
    position: absolute;
    width: 6px;
  }

  @media (max-width: 768px) {
    li:nth-child(odd) {
      align-self: flex-end;
      justify-content: flex-start;
    }

    li:nth-child(odd)::after,
    li:nth-child(even)::after {
      left: 18px;
    }

    li:nth-child(odd)::before,
    li:nth-child(even)::before {
      border-color: transparent white transparent transparent;
      border-width: 10px 10px 10px 0;
      left: 60px;
      right: unset;
    }

    ::after {
      left: 31px;
    }
  }
`;

export { Timeline, TimelineItem };
