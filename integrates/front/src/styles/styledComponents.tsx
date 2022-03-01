import { NavLink } from "react-router-dom";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import style from "utils/forms/index.css";

const Alert: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs(
  {
    className:
      "b--salmon bg-salmon br3 burgundy mb3 outline-transparent pb2 pt2 pl3 pr3",
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
  className: "flex flex-wrap items-center justify-end",
})``;

const CheckBox: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `br0 relative checkbox-mh w-100 flex bg-white b--moon-gray`,
})``;

const CheckBoxOption: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs(
  (props: {
    theme: {
      selected: boolean;
      type: string;
    };
  }): {
    className: string;
  } => ({
    className: `absolute ba bottom-0 top-0 tc pv2 white ${
      props.theme.type === "yes"
        ? "green-checkbox left-0"
        : "red-checkbox right-0"
    } ${props.theme.selected ? "w-100" : "w-50"} `,
  })
)``;

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

const Col50Ph: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "w-50-ns",
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
  className: "f5 w-fit-content ws-pre-wrap ma0",
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

const Filters = styled.div.attrs({
  className: "flex flex-wrap flex-auto mt2",
})``;

const Flex: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs<{
  className: string;
}>({
  className: "flex flex-wrap",
})``;

const FlexAutoContainer = styled.div.attrs({
  className: "flex-auto mh1 mv1",
})``;

const FormGroup: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "mb4 w-100",
})``;

const HintFieldText: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "w-auto mb1 mh1",
})``;

const GraphicButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs(
  ({
    className,
    type,
  }): Partial<React.ButtonHTMLAttributes<HTMLButtonElement>> => ({
    className: `dim dib g-btn pointer pr3 pl3 pt2 pb2 outline-0 ${
      className ?? ""
    }`,
    type: type ?? "button",
  })
)``;

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

const LastGroupSetting: StyledComponent<
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

const MenuItem: StyledComponent<
  "li",
  Record<string, unknown>
> = styled.li.attrs({
  className: `
  ba br0 db overflow-hidden ph3 pointer pv2 relative switch-mh tc w-100 bg-white b--white
  `,
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
  className: "color-inherit fw3 f3 lh-solid ma0 tc",
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

const GroupScopeText: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "ph1-5 vertical-center w-60-ns fw2 f5",
})``;

const GroupScopeTextWide: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "ph1-5 vertical-center w-75 fw2 f5",
})``;

const QuestionButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs(
  ({
    className,
    type,
  }): Partial<React.ButtonHTMLAttributes<HTMLButtonElement>> => ({
    className: `outline-0 pa0 questionBtn ${className ?? ""}`,
    type: type ?? "button",
  })
)``;

const Radio: StyledComponent<
  "input",
  Record<string, unknown>
> = styled.input.attrs({
  className: `
    op7
    dn
    transparent
  `,
  type: `radio`,
})``;

const RadioLabel: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs(
  (props: {
    theme: { on: boolean; color: string };
  }): {
    className: string;
  } => ({
    className: `ba br0 db overflow-hidden ph3 pointer pv2 relative switch-mh tc w-100 ${
      props.theme.on ? props.theme.color : "bg-white b--moon-gray"
    }`,
  })
)``;

const RangeContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "flex flex-wrap",
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
  className: "flex justify-center mt4 w-20",
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

const Select = styled.select.attrs({
  className: `${style["form-control"]} black-40 border-box`,
})``;

const Small: StyledComponent<
  "small",
  Record<string, unknown>
> = styled.small.attrs({
  className: "justify-center ph1 pv0",
})``;

const SelectContainer = styled.div.attrs({
  className: "flex-auto mh1 mw6 mv1",
})``;

const InputText = styled.input.attrs({
  className: `${style["form-control"]} black-40 border-box`,
})``;

const InputRange = styled.input.attrs({
  className: `${style["form-control"]} black-40 center border-box mw4`,
})``;

const InputDateRange = styled.input.attrs({
  className: `${style["form-control"]} black-40 border-box mw5`,
})``;

const InputNumber = styled.input.attrs({
  className: `${style["form-control"]} black-40 border-box`,
})``;

const SearchText = styled.input.attrs({
  className: `${style["form-control"]} black-40 border-box pv2`,
})``;

const SelectDate = styled.input.attrs({
  className: `${style["form-control"]} black-40 border-box`,
  type: `date`,
})``;

const Switch: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs(
  (props: {
    theme: { on: boolean; color: string };
  }): {
    className: string;
  } => ({
    className: `ba br0 db overflow-hidden ph3 pointer pv2 relative switch-mh tc w-100 ${
      props.theme.on ? props.theme.color : "bg-white b--moon-gray"
    }`,
  })
)``;

const SwitchHandle: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs({
  className: "bg-white br0 dib h-100 ma0 relative ph1-5",
})``;

const SwitchGroup: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs(
  (props: {
    theme: { on: boolean };
  }): {
    className: string;
  } => ({
    className: `absolute bottom-0 top-0 right-0 switch-transition tc w-200 ${
      props.theme.on ? "left-0 " : "left--100"
    }`,
  })
)``;

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

const Tab = styled(NavLink)`
  color: #b0b0bf;
  font-size: 20px;
  padding-bottom: 12px;
  text-decoration: none;

  &.active {
    border-bottom: 2px solid #5c5c70;
    color: #2e2e38;
  }

  :hover {
    color: #2e2e38;
  }
`;

const TabContent = styled.div.attrs({
  className: "mt3",
})``;

const TableOptionsColBar: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "dib ma0 pa0 w-20",
})``;

const TabsContainer = styled.ul.attrs({
  className: "flex justify-around list ma0",
})`
  background-color: #f4f4f6;
  padding: 12px 0;
`;

const TrackingLabel: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: "f5 mv0 w-fit-content ws-pre-wrap ww-break-word",
})``;

const Well: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs<{
  className: string;
}>({
  className: "well pa4 mb4",
})``;

export {
  Alert,
  ButtonGroup,
  ButtonToolbar,
  ButtonToolbarCenter,
  ButtonToolbarLeft,
  ButtonToolbarRow,
  CheckBox,
  CheckBoxOption,
  Col100,
  Col25,
  Col33,
  Col40,
  Col45,
  Col50,
  Col50Ph,
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
  Filters,
  Flex,
  FlexAutoContainer,
  FormGroup,
  HintFieldText,
  InputDateRange,
  InputNumber,
  InputRange,
  InputText,
  GraphicButton,
  GraphicPanelCollapse,
  GraphicPanelCollapseBody,
  GraphicPanelCollapseHeader,
  InputGroup,
  Label,
  LastGroupSetting,
  MenuItem,
  Meter,
  ModalBody,
  ModalFooter,
  ModalHeader,
  ModalTitle,
  Panel,
  PanelBody,
  PanelCollapse,
  PanelCollapseBody,
  PanelCollapseHeader,
  GroupScopeText,
  GroupScopeTextWide,
  QuestionButton,
  Radio,
  RadioLabel,
  RangeContainer,
  RemoveItem,
  RemoveTag,
  RequiredField,
  Row,
  RowCenter,
  Small,
  SearchText,
  Select,
  SelectContainer,
  SelectDate,
  Switch,
  SwitchHandle,
  SwitchGroup,
  SwitchOff,
  SwitchOn,
  Tab,
  TabContent,
  TableOptionsColBar,
  TabsContainer,
  TrackingLabel,
  Well,
};
