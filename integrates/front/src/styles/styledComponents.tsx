import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const Alert: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs(
  {
    className: "b--salmon bg-salmon br3 burgundy mb4 outline-transparent pa3",
  }
)``;

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
  className: "breadcrumb",
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
  className: "f3 w-fit-content ws-pre-wrap ww-break-word",
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

const InfoButtonBitbucket: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className:
    "dim w-100 db ba br0 outline-0 btn-loginInfo btn-bitbucketLoginInfo",
})``;

const InfoButtonGoogle: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: "dim w-100 db ba br0 outline-0 btn-loginInfo btn-googleLoginInfo",
})``;

const InfoButtonMicrosoft: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className:
    "dim w-100 db ba br0 outline-0 btn-loginInfo btn-microsoftLoginInfo",
})``;

const Label: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs({
  className: "bg-lbl-gray br2 f4 fw7 ml3 nowrap pv1 ph2 tc white",
})``;

const LoginButtonBitbucket: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className:
    "dim w-100 flex ba br0 pa3 mt2 outline-0 justify-between items-center btn-login btn-bitbucketLoginInfo",
})``;

const LoginButtonGoogle: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className:
    "dim w-100 flex ba br0 pa3 mt5 outline-0 justify-between items-center btn-login btn-googleLoginInfo",
})``;

const LoginButtonMicrosoft: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className:
    "dim w-100 flex ba br0 pa3 mt2 outline-0 justify-between items-center btn-login btn-microsoftLoginInfo",
})``;

const LoginCommit: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "absolute commit",
})``;

const LoginContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "items-center flex flex-row white h-100",
})``;

const LoginDeploymentDate: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "absolute deploymentDate",
})``;

const LoginGrid: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "login-grid center pa2",
})``;

const LoginRow: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "cf pa1-ns content-center tc",
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
  className: "bg-ne modalh-bb pv4 ph3 white",
})``;

const ModalTitle: StyledComponent<
  "h4",
  Record<string, unknown>
> = styled.h4.attrs({
  className: "color-inherit fw3 f2 lh-solid ma0 montserrat tc",
})``;

const NavBar: StyledComponent<
  "nav",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "ph4 navbar h-100",
})``;

const NavBarCollapse: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "flex items-center nav-collapse",
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

const Notification2FaCol: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "fl w-100 w-third-ns pa2",
})``;

const Notification2FaGrid: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "mw9 center pa2-ns",
})``;

const Notification2FaRow: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "cf flex pa1-ns",
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
  Alert,
  BreadCrumb,
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
  Container,
  ControlLabel,
  EditableFieldContent,
  EditableFieldNotUrl,
  EditableFieldTitle25,
  EditableFieldTitle50,
  EventHeaderGrid,
  EventHeaderLabel,
  ExpandableLabel,
  FindingHeaderDetail,
  FindingHeaderGrid,
  FindingHeaderIndicator,
  FindingHeaderLabel,
  FormGroup,
  InfoButtonBitbucket,
  InfoButtonGoogle,
  InfoButtonMicrosoft,
  Label,
  LoginButtonBitbucket,
  LoginButtonGoogle,
  LoginButtonMicrosoft,
  LoginCommit,
  LoginContainer,
  LoginDeploymentDate,
  LoginGrid,
  LoginRow,
  Meter,
  ModalBody,
  ModalFooter,
  ModalHeader,
  ModalTitle,
  NavBar,
  NavBarCollapse,
  NavBarHeader,
  NavItem,
  Notification2FaCol,
  Notification2FaGrid,
  Notification2FaRow,
  Panel,
  PanelBody,
  ProgressBar,
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
  TabsContainer,
};
