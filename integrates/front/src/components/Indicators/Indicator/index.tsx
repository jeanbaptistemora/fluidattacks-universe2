import styled from "styled-components";

const Indicator = styled.div.attrs({ className: "tc w-20" })``;
const IndicatorIcon = styled.div`
  color: #b0b0bf;
  font-size: 2rem;
`;
const IndicatorTitle = styled.div.attrs({ className: "pa3" })``;
const IndicatorValue = styled.h1``;

export { Indicator, IndicatorIcon, IndicatorTitle, IndicatorValue };
