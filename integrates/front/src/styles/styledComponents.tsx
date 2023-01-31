import type { StyledComponent } from "styled-components";
import styled from "styled-components";

/**
 * This is a legacy file and is set to dissapear eventually.
 * New generic and reusable components should be created in src/components
 * or in a styles.ts file in the same directory if its very specific to the view.
 */

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

const Col50: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "ph1-5 w-50-ns",
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
  Col50,
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
  InputGroup,
  PanelCollapseBody,
  PanelCollapseHeader,
  Radio,
  RadioLabel,
  RemoveTag,
  RequiredField,
  Row,
  RowCenter,
  SwitchItem,
  TabContent,
};
