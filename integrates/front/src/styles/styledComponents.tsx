import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const Alert: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs(
  {
    className: "b--salmon bg-salmon br3 burgundy mb4 outline-transparent pa3",
  }
)``;

const ButtonGroup: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "relative dib",
})``;

const ButtonToolbar: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "fr",
})``;

const ButtonToolbarCenter: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "flex flex-wrap justify-center pv3 w-100",
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

const BreadCrumb: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "breadcrumb list mt3",
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

const Col33: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "ph1-5 w-33-ns",
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

const Col50: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "ph1-5 w-50-ns",
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

const Col33L: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "w-33-l",
})``;

const Container: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "center ph1-5",
})``;

const ControlLabel: StyledComponent<
  "label",
  Record<string, unknown>
> = styled.label.attrs({
  className: "dib fw4 mb2",
})``;

const EditableFieldContent: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "w-auto",
})``;

const EditableFieldNotUrl: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: "f5 w-fit-content ws-pre-wrap ww-break-word ma0",
})``;

const EditableFieldTitle25: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "ph1-5 tr w-25-ns",
})``;

const EditableFieldTitle50: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "ph1-5 tr w-50-ns",
})``;

const EvidenceDescription: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "f5 w-100",
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

const ExpandableLabel: StyledComponent<
  "label",
  Record<string, unknown>
> = styled.label.attrs({
  className: "b pointer",
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
  className: "grid ph4 menu-grid mb2",
})``;

const FindingHeaderIndicator: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: "f3 ma0",
})``;

const FindingHeaderLabel: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: "ma0",
})``;

const Flex: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs<{
  className: string;
}>({
  className: "flex flex-wrap",
})``;

const FormGroup: StyledComponent<
  "form",
  Record<string, unknown>
> = styled.form.attrs({
  className: "mb4 w-100",
})``;

const GraphicButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: "dim dib g-btn pr3 pl3 pt2 pb2 outline-0",
})``;

const GraphicPanelCollapse: StyledComponent<
  "div",
  Record<string, boolean>
> = styled.div.attrs({
  className: "mb4 items-center",
})``;

const GraphicPanelCollapseBody: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "pa2 items-center panel-cb",
})``;

const GraphicPanelCollapseHeader: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "pb3 pl4 pt3 pr4 items-center panel-ch",
})``;

const GraphicPanelCollapseFooter: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "pb3 pl4 pt3 pr4 items-center panel-cf",
})``;

const InputGroup: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs({
  className: "relative dt",
})``;

const Label: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs({
  className: "bg-lbl-gray br2 f4 fw7 ml3 nowrap pv1 ph2 tc white",
})``;

const LastProjectSetting: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "mb10",
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
  className: "modalf-bt pa1-5 tr",
})``;

const ModalHeader: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "bg-orgred modalh-bb pv3 ph2 white",
})``;

const ModalTitle: StyledComponent<
  "h4",
  Record<string, unknown>
> = styled.h4.attrs({
  className: "color-inherit fw3 f3 lh-solid ma0 montserrat tc",
})``;

const NavBar: StyledComponent<
  "nav",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "ph4 pt0 pb0 navbar h-100",
})``;

const NavBarCollapse: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "flex items-center nav-collapse",
})``;

const NavBarForm: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "navbar-form",
})``;

const NavBarFormGroup: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "nav-group flex items-center",
})``;

const NavBarHeader: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "flex navbar-header",
})``;

const NavItem: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "nav-item",
})``;

const NavSplitButtonContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "split-button",
})``;

const Panel: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs(
  {
    className: "b--mid-light-gray ba bg-white br2 mb4",
  }
)``;

const PanelBody: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "pa1-5",
})``;

const PanelCollapse: StyledComponent<
  "div",
  Record<string, boolean>
> = styled.div.attrs({
  className: "mb4 items-center hide-child panel-c",
})``;

const PanelCollapseBody: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "child pa4 items-center panel-cb",
})``;

const PanelCollapseHeader: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "pb3 pl4 pt3 pr4 items-center tc panel-ch",
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

const ProjectScopeText: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "ph1-5 vertical-center w-60-ns fw2 f4",
})``;

const QuestionButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: "outline-0 pa0 questionBtn",
})``;

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
  className: "flex flex-wrap",
})``;

const RowCenter: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "flex flex-wrap justify-center",
})``;

const StickyContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "bg-white sticky z-4",
})``;

const StickyContainerFinding: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "bg-white sticky-find z-4",
})``;

const StickyContainerOrg: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "bg-white w-100 sticky z-4",
})``;

const Switch: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs((props: { theme: { on: boolean; color: string } }): {
  className: string;
} => ({
  className: `ba br0 db overflow-hidden ph3 pointer pv2 relative switch-mh tc w-100 ${
    props.theme.on ? props.theme.color : "bg-white b--moon-gray"
  }`,
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
  className: `absolute bottom-0 top-0 right-0 switch-transition tc w-200 ${
    props.theme.on ? "left-0 " : "left--100"
  }`,
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
  className: "a-bg-white a-db a-gray a-pv a-relative tc nowrap",
})``;

const TabContent: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "bg-white pa4 mb5",
})``;

const TableOptionsColBar: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "dib ma0 pa0 w-60-ns",
})``;

const TableOptionsColBtn: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "dib pa0 w-40-ns table-btn",
})``;

const TabsContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "grid mb0 menu-grid pl0 tc-shadow w-100",
})``;

const TrackingLabel: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: "f5 mv0 w-fit-content ws-pre-wrap ww-break-word",
})``;

const ValidationError: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "dark-red",
})``;

const Well: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs<{
  className: string;
}>({
  className: "well pa4 mb4",
})``;

export {
  Alert,
  BreadCrumb,
  ButtonGroup,
  ButtonToolbar,
  ButtonToolbarCenter,
  ButtonToolbarLeft,
  ButtonToolbarRow,
  Col100,
  Col25,
  Col33,
  Col40,
  Col45,
  Col50,
  Col60,
  Col80,
  Col33L,
  Container,
  ControlLabel,
  EditableFieldContent,
  EditableFieldNotUrl,
  EditableFieldTitle25,
  EditableFieldTitle50,
  EventHeaderGrid,
  EventHeaderLabel,
  EvidenceDescription,
  ExpandableLabel,
  FindingHeaderDetail,
  FindingHeaderGrid,
  FindingHeaderIndicator,
  FindingHeaderLabel,
  Flex,
  FormGroup,
  GraphicButton,
  GraphicPanelCollapse,
  GraphicPanelCollapseBody,
  GraphicPanelCollapseFooter,
  GraphicPanelCollapseHeader,
  InputGroup,
  Label,
  LastProjectSetting,
  Meter,
  ModalBody,
  ModalFooter,
  ModalHeader,
  ModalTitle,
  NavBar,
  NavBarCollapse,
  NavBarForm,
  NavBarFormGroup,
  NavBarHeader,
  NavItem,
  NavSplitButtonContainer,
  Panel,
  PanelBody,
  PanelCollapse,
  PanelCollapseBody,
  PanelCollapseHeader,
  ProgressBar,
  ProjectScopeText,
  QuestionButton,
  RemoveItem,
  RemoveTag,
  RequiredField,
  Row,
  RowCenter,
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
  TableOptionsColBar,
  TableOptionsColBtn,
  TabsContainer,
  TrackingLabel,
  ValidationError,
  Well,
};
