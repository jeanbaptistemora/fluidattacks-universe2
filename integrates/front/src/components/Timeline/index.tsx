/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

const Timeline = styled.div.attrs({
  className: "comp-timeline",
})`
  display: flex;
  flex-direction: column;
  position: relative;

  ::before {
    background-color: #d2d2da;
    border-radius: 4px;
    height: 100%;
    width: 6px;
  }

  > * {
    max-width: 45%;
    max-width: calc(50% - 24px);
    min-width: 40%;
    :nth-child(even) {
      align-self: end;
    }
    :nth-child(odd) {
      align-self: start;
    }

    ::before {
      background-color: #bf0b1a;
      border-radius: 50%;
      height: 16px;
      width: 16px;
      z-index: 1;
    }
  }

  ::before,
  > *::before {
    content: "";
    left: 50%;
    position: absolute;
    transform: translateX(-50%);
  }

  @media (max-width: 768px) {
    ::before,
    > *::before {
      left: 8px;
    }

    > * {
      margin: 12px 0;
      max-width: 95%;
      max-width: calc(100% - 32px);
      min-width: 85%;
      :nth-child(odd) {
        align-self: end;
      }
    }
  }
`;

export { Timeline };
