import styled, { StyledComponent } from "styled-components";

const ButtonToolbar: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "fr",
})``;

const ModalBody: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "relative pa4",
})``;

const ModalFooter: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "modalf-bt modalf-pa tr",
})``;

const ModalHeader: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "bg-ne modalh-bb pv4 ph3 white",
})``;

const ModalTitle: StyledComponent<
  "h4",
  Record<string, unknown>
> = styled.h4.attrs({
  className: "color-inherit fw3 f2 lh-solid ma0 montserrat tc",
})``;

const RequiredField: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs<{
  className: string;
}>({
  className: "orgred",
})``;

const Row: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs<{
  className: string;
}>({
  className: "mh--15 flex",
})``;

const StickyContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "bg-white sticky top5-5 top9-9 z-4",
})``;

const StickyContainerFinding: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "bg-white sticky-find top9-9 top5-5-find z-4",
})``;

const StickyContainerOrg: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "bg-white sticky top5-5 z-4",
})``;

const Tab: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs<{
  className: string;
}>({
  className: "a-bg-white a-db a-gray a-pv a-relative tc",
})``;

const TabsContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "grid mb0 menu-grid pl0 tc-shadow w-100",
})``;

export {
  ButtonToolbar,
  ModalBody,
  ModalFooter,
  ModalHeader,
  ModalTitle,
  RequiredField,
  Row,
  StickyContainer,
  StickyContainerFinding,
  StickyContainerOrg,
  Tab,
  TabsContainer,
};
