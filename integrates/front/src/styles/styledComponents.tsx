import styled, { StyledComponent } from "styled-components";

const ButtonToolbar: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "fr",
})``;

const Col100: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "ph1-5 w-100",
})``;

const Col40: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "ph1-5 w-40",
})``;

const ControlLabel: StyledComponent<
  "label",
  Record<string, unknown>
> = styled.label.attrs({
  className: "dib fw4 mb2",
})``;

const EventHeaderGrid: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "grid ma4 menu-grid",
})``;

const EventHeaderLabel: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "ph3 tc",
})``;

const FormGroup: StyledComponent<
  "form",
  Record<string, unknown>
> = styled.form.attrs({
  className: "mb4 w-100",
})``;

const Label: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs({
  className: "bg-lbl-gray br2 f4 fw7 ml3 nowrap pv1 ph2 tc white",
})``;

const Meter: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs(
  {
    className: "bg-light-gray br3 h2 meter-shadow relative",
  }
)``;

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

const ProgressBar: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className:
    "br3 db f3 h-100 bg-red bg-size4 overflow-hidden pb-animation pb-bi pb-transition relative tc white",
})`
  width: ${(props: { theme: { width: string } }): string => props.theme.width};
`;

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

const TabContent: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "bg-white pa4 mb5",
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
  Col100,
  Col40,
  ControlLabel,
  EventHeaderGrid,
  EventHeaderLabel,
  FormGroup,
  Label,
  Meter,
  ModalBody,
  ModalFooter,
  ModalHeader,
  ModalTitle,
  ProgressBar,
  RequiredField,
  Row,
  StickyContainer,
  StickyContainerFinding,
  StickyContainerOrg,
  Tab,
  TabContent,
  TabsContainer,
};
