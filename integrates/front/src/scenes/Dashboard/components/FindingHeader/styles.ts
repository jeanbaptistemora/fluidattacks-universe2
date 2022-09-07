/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

const FindingHeaderContainer = styled.div.attrs({
  className: "flex flex-wrap justify-around mb2",
})``;

const FindingHeaderDetail = styled.div.attrs({
  className: "flex flex-auto items-center justify-center",
})``;

const FindingHeaderLabel = styled.p.attrs({
  className: "ml2 ma0",
})``;

const FindingHeaderIndicator = styled.p.attrs({
  className: "f3 ma0",
})``;

export {
  FindingHeaderContainer,
  FindingHeaderDetail,
  FindingHeaderIndicator,
  FindingHeaderLabel,
};
