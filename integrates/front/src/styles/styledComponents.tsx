import styled, { StyledComponent } from "styled-components";

const ButtonToolbar: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "fr",
})``;

const ButtonToolbarLeft: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "fl",
})``;

const ButtonToolbarRow: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "flex flex-wrap justify-end",
})``;

const Col100: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "ph1-5 w-100",
})``;

const Col25: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "ph1-5 w-25-ns",
})``;

const Col40: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "ph1-5 w-40-ns",
})``;

const Col45: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "ph1-5 w-45-ns",
})``;

const Col60: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "ph1-5 w-60-ns",
})``;

const Col80: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "ph1-5 w-80",
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

const FindingHeaderDetail: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "ph1-5 tc",
})``;

const FindingHeaderGrid: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "grid ph4 menu-grid",
})``;

const FindingHeaderIndicator: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: "f2",
})``;

const FindingHeaderLabel: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: "mb0",
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

const RemoveItem: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "mt5 ml40",
})``;

const RemoveTag: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "flex justify-center mt-3-25 w-20",
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
  className: "mh--15 flex flex-wrap",
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

const Switch: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs((props: { theme: { on: boolean } }): {
  className: string;
} => ({
  className:
    "ba br0 db overflow-hidden ph3 pointer pv2 relative switch-mh tc w-100 " +
    (props.theme.on ? "bg-switch b--switch" : "bg-white b--moon-gray"),
}))``;

const SwitchHandle: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs({
  className: "bg-white br0 dib h-100 ma0 relative ph1-5",
})``;

const SwitchGroup: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs((props: { theme: { on: boolean } }): {
  className: string;
} => ({
  className:
    "absolute bottom-0 top-0 right-0 switch-transition tc w-200 " +
    (props.theme.on ? "left-0 " : "left--100"),
}))``;

const SwitchOff: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs({
  className:
    "absolute bg-white bottom-0 br0 dib l-50 ma0 mid-gray ph3 pv2 right-0 top-0",
})``;

const SwitchOn: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs({
  className:
    "absolute bg-switch bottom-0 br0 left-0 ma0 ph3 pv2 r-50 top-0 white",
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
  ButtonToolbarLeft,
  ButtonToolbarRow,
  Col100,
  Col25,
  Col40,
  Col45,
  Col60,
  Col80,
  ControlLabel,
  EventHeaderGrid,
  EventHeaderLabel,
  FindingHeaderDetail,
  FindingHeaderGrid,
  FindingHeaderIndicator,
  FindingHeaderLabel,
  FormGroup,
  Label,
  Meter,
  ModalBody,
  ModalFooter,
  ModalHeader,
  ModalTitle,
  ProgressBar,
  RemoveItem,
  RemoveTag,
  RequiredField,
  Row,
  StickyContainer,
  StickyContainerFinding,
  StickyContainerOrg,
  Switch,
  SwitchHandle,
  SwitchGroup,
  SwitchOff,
  SwitchOn,
  Tab,
  TabContent,
  TabsContainer,
};
