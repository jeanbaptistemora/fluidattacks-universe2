/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import { faMagnifyingGlass, faXmark } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { Meta, Story } from "@storybook/react";
import { Form, Formik } from "formik";
import React from "react";
import { object, string } from "yup";

import type { IInputProps } from "./CustomInput";
import type { ISelectProps } from "./CustomSelect";
import type { ITextAreaProps } from "./CustomTextArea";
import type { IDatePickerProps } from "./DatePicker";
import type { IInputNumberProps } from "./InputNumber";

import {
  DatePicker as DatePickerComp,
  Input,
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
      <Input {...props} id={"ExampleId"} name={"exampleName"} />
    </Form>
  </Formik>
);

const StoryDatePicker: Story<IDatePickerProps> = (props): JSX.Element => (
  <Formik
    initialValues={{ exampleName: "" }}
    name={"exampleForm"}
    onSubmit={handleSubmit}
  >
    <Form id={"exampleForm"}>
      <DatePickerComp {...props} id={"ExampleId"} name={"exampleName"} />
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
      <InputNumberComp {...props} id={"ExampleId"} name={"exampleName"} />
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
      <SelectComp {...props} id={"ExampleId"} name={"exampleName"} />
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
      <TextAreaComp {...props} id={"ExampleId"} name={"exampleName"} />
    </Form>
  </Formik>
);

const Default = StoryDefault.bind({});
Default.args = {
  disabled: false,
  label: "ExampleLabel",
  placeholder: "Example placeholder",
  variant: "solid",
};

const DatePicker = StoryDatePicker.bind({});

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

export { Default, DatePicker, InputNumber, Search, Select, TextArea };
export default config;
