/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import { faMagnifyingGlass, faXmark } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { Meta, Story } from "@storybook/react";
import { Form, Formik } from "formik";
import React from "react";
import { object, string } from "yup";

import type { IInputDateTimeProps } from "./Formik";

import type {
  ICheckboxProps,
  IEditableProps,
  IInputArrayProps,
  IInputDateProps,
  IInputNumberProps,
  IInputProps,
  ISelectProps,
  ITextAreaProps,
} from ".";
import {
  Checkbox as CheckboxComp,
  DataList,
  Editable as EditableComp,
  Input,
  InputArray as InputArrayComp,
  InputDate as InputDateComp,
  InputDateTime as InputDateTimeComp,
  InputNumber as InputNumberComp,
  Select as SelectComp,
  TextArea as TextAreaComp,
} from ".";
import { Button } from "components/Button";
import { Logger } from "utils/logger";

const config: Meta = {
  component: Input,
  title: "components/Input",
};

interface IFormValues {
  exampleName: string;
}

const handleSubmit = ({ exampleName }: IFormValues): void => {
  Logger.warning(exampleName);
};

const validations = object().shape({
  exampleName: string()
    .required("Field required")
    .max(8, "Use less characters")
    .matches(/^[a-zA-Z_0-9-]{1,8}$/u, "Allowed alphanumeric characters only"),
});

const validationsInputNumber = object().shape({
  exampleName: string().required().min(-10).max(10),
});

const selectValidations = object().shape({
  exampleName: string().required(),
});

const StoryDefault: Story<IInputProps> = (props): JSX.Element => (
  <Formik
    initialValues={{ exampleName: "" }}
    name={"exampleForm"}
    onSubmit={handleSubmit}
    validationSchema={validations}
  >
    <Form id={"exampleForm"}>
      <Input {...props} id={"ExInput"} list={"ExList"} name={"exampleName"} />
      <DataList data={["abc", "bcd", "cde", "ab", "bc", "cd"]} id={"ExList"} />
    </Form>
  </Formik>
);

const StoryCheckbox: Story<ICheckboxProps> = (props): JSX.Element => (
  <Formik
    initialValues={{ exampleName: "" }}
    name={"exampleForm"}
    onSubmit={handleSubmit}
    validationSchema={validations}
  >
    <Form id={"exampleForm"}>
      <CheckboxComp {...props} id={"ExCheckbox"} name={"exampleName"} />
    </Form>
  </Formik>
);

const StoryInputArray: Story<IInputArrayProps> = (props): JSX.Element => (
  <Formik
    initialValues={{ exampleName: "" }}
    name={"exampleForm"}
    onSubmit={handleSubmit}
    validationSchema={validations}
  >
    <Form id={"exampleForm"}>
      <InputArrayComp {...props} id={"ExInput"} name={"exampleName"} />
    </Form>
  </Formik>
);

const StoryInputDate: Story<IInputDateProps> = (props): JSX.Element => (
  <Formik
    initialValues={{ exampleName: "" }}
    name={"exampleForm"}
    onSubmit={handleSubmit}
  >
    <Form id={"exampleForm"}>
      <InputDateComp {...props} id={"ExInputDate"} name={"exampleName"} />
    </Form>
  </Formik>
);

const StoryInputNumber: Story<IInputNumberProps> = (props): JSX.Element => (
  <Formik
    initialValues={{ exampleName: "" }}
    name={"exampleForm"}
    onSubmit={handleSubmit}
    validationSchema={validationsInputNumber}
  >
    <Form id={"exampleForm"}>
      <InputNumberComp {...props} id={"ExInputNumber"} name={"exampleName"} />
    </Form>
  </Formik>
);

const StorySelect: Story<ISelectProps> = (props): JSX.Element => (
  <Formik
    initialValues={{ exampleName: "" }}
    name={"exampleForm"}
    onSubmit={handleSubmit}
    validationSchema={selectValidations}
  >
    <Form id={"exampleForm"}>
      <SelectComp {...props} id={"ExSelect"} name={"exampleName"} />
    </Form>
  </Formik>
);

const StoryTextArea: Story<ITextAreaProps> = (props): JSX.Element => (
  <Formik
    initialValues={{ exampleName: "" }}
    name={"exampleForm"}
    onSubmit={handleSubmit}
    validationSchema={validations}
  >
    <Form id={"exampleForm"}>
      <TextAreaComp {...props} id={"ExTextarea"} name={"exampleName"} />
    </Form>
  </Formik>
);

const StoryEditable: Story<IEditableProps> = (
  props: Readonly<IEditableProps>
): JSX.Element => {
  const { label } = props;

  return (
    <Formik
      initialValues={{ exampleName: "" }}
      name={"exampleForm"}
      onSubmit={handleSubmit}
      validationSchema={validations}
    >
      <Form id={"exampleForm"}>
        <EditableComp {...props}>
          <Input id={"ExInput"} label={label} name={"exampleName"} />
        </EditableComp>
      </Form>
    </Formik>
  );
};

const StoryInputDateTime: Story<IInputDateTimeProps> = (props): JSX.Element => (
  <Formik
    initialValues={{ exampleName: "" }}
    name={"exampleForm"}
    onSubmit={handleSubmit}
    validationSchema={validations}
  >
    <Form id={"exampleForm"}>
      <InputDateTimeComp {...props} id={"ExInput"} name={"exampleName"} />
    </Form>
  </Formik>
);

const Default = StoryDefault.bind({});
Default.args = {
  disabled: false,
  label: "ExampleLabel",
  placeholder: "Example placeholder",
  required: false,
  tooltip: "Example tooltip",
  variant: "solid",
};

const Checkbox = StoryCheckbox.bind({});
Checkbox.args = {
  label: "Example label",
  required: true,
  tooltip: "Example tooltip",
};

const InputArray = StoryInputArray.bind({});
InputArray.args = {
  disabled: false,
  label: "ExampleLabel",
  placeholder: "Example placeholder",
  required: false,
  tooltip: "Example tooltip",
  variant: "solid",
};

const InputDate = StoryInputDate.bind({});

const InputNumber = StoryInputNumber.bind({});
InputNumber.args = {
  disabled: false,
  label: "ExampleLabel",
  max: 10,
  min: -10,
  placeholder: "Example placeholder",
  variant: "solid",
};

const Search = StoryDefault.bind({});
Search.args = {
  childLeft: (
    <Button size={"sm"}>
      <FontAwesomeIcon icon={faMagnifyingGlass} />
    </Button>
  ),
  childRight: (
    <Button size={"sm"}>
      <FontAwesomeIcon icon={faXmark} />
    </Button>
  ),
  placeholder: "Example placeholder",
  variant: "solid",
};

const Select = StorySelect.bind({});
Select.args = {
  children: (
    <React.Fragment>
      {[...Array(7).keys()].map(
        (el): JSX.Element => (
          <option key={el} value={el}>{`Option ${el}`}</option>
        )
      )}
    </React.Fragment>
  ),
  disabled: false,
  label: "ExampleLabel",
  variant: "solid",
};

const TextArea = StoryTextArea.bind({});
TextArea.args = {
  disabled: false,
  label: "ExampleLabel",
  placeholder: "Example placeholder",
  rows: 3,
  variant: "solid",
};

const Editable = StoryEditable.bind({});
Editable.args = {
  currentValue: "Example value",
  isEditing: false,
  label: "Example label",
};

const InputDateTime = StoryInputDateTime.bind({});
InputDateTime.args = {
  disabled: false,
  label: "ExampleLabel",
  required: false,
  tooltip: "Example tooltip",
  variant: "solid",
};

export {
  Default,
  Checkbox,
  Editable,
  InputArray,
  InputDate,
  InputDateTime,
  InputNumber,
  Search,
  Select,
  TextArea,
};
export default config;
