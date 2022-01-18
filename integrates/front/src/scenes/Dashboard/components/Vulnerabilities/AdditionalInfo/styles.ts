import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const OuterRow: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "flex flex-wrap pb1",
})``;

const Row: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs<{
  className: string;
}>({
  className: "flex flex-wrap-m pb1",
})``;

const LabelField: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "pl1 pr0 w-30-l w-100-m w-100-ns w-auto",
})``;

const InfoField: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "pl1 pr0 w-70-l w-100-m w-100-ns w-auto",
})``;

const Col100: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "pl1 pr0 pb1 w-100",
})``;

const Col50: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "w-50-l w-50-m w-100-ns",
})``;

const Field: StyledComponent<"p", Record<string, unknown>> = styled.p.attrs({
  className: "lh-title ma0 mid-gray w-fit-content ws-pre-wrap ww-break-word",
})``;

const Label: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs({
  className: "black f5 lh-title fw5",
})``;

const Status: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs({
  className: "f2-5",
})``;

export {
  OuterRow,
  Row,
  LabelField,
  InfoField,
  Col100,
  Col50,
  Field,
  Label,
  Status,
};
