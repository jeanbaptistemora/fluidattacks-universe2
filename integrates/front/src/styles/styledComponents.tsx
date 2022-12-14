import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import style from "utils/forms/index.css";

const ButtonToolbarCenter: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "flex flex-wrap justify-center pv3 w-100",
})``;

const ButtonToolbarRow: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "flex flex-wrap items-center justify-end",
})``;

const ButtonToolbarStartRow: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "flex flex-wrap items-center justify-start",
})``;

const CheckBox: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `br0 relative checkbox-mh w-100 flex b--moon-gray`,
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

const Col33: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "ph1-5 w-33-ns",
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
  className: "ph3 flex items-center panel-ch",
})`
  height: 67px;
`;

const InputGroup: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs({
  className: "relative dt",
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
      props.theme.on ? props.theme.color : "b--moon-gray"
    }`,
  })
)``;

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

const Small: StyledComponent<
  "small",
  Record<string, unknown>
> = styled.small.attrs({
  className: "justify-center ph1 pv0",
})``;

const SearchText = styled.input.attrs({
  className: `${style["form-control"]} black-40 border-box pv2`,
})``;

const SwitchItem: StyledComponent<
  "li",
  Record<string, unknown>
> = styled.li.attrs({
  className: `
  br0 db overflow-hidden pointer pa0 ma0 relative switch-mh tc w-100
  `,
})``;

const TabContent = styled.div.attrs({
  className: "mt3",
})``;

export {
  ButtonToolbarCenter,
  ButtonToolbarRow,
  ButtonToolbarStartRow,
  CheckBox,
  CheckBoxOption,
  Col100,
  Col33,
  Col45,
  Col50,
  Col60,
  Col80,
  ControlLabel,
  EditableFieldContent,
  EditableFieldNotUrl,
  EditableFieldTitle25,
  EditableFieldTitle50,
  EventHeaderGrid,
  EventHeaderLabel,
  EvidenceDescription,
  FormGroup,
  HintFieldText,
  GraphicButton,
  GraphicPanelCollapse,
  GraphicPanelCollapseBody,
  GraphicPanelCollapseHeader,
  InputGroup,
  PanelCollapseBody,
  PanelCollapseHeader,
  QuestionButton,
  Radio,
  RadioLabel,
  RemoveTag,
  RequiredField,
  Row,
  RowCenter,
  Small,
  SearchText,
  SwitchItem,
  TabContent,
};
