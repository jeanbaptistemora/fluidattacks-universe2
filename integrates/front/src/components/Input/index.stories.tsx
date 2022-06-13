/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import { Form, Formik } from "formik";
import React from "react";
import { object, string } from "yup";

import type { IInputProps } from "./CustomInput";

import { Input } from ".";
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

const Template: Story<IInputProps> = (props): JSX.Element => (
  <Formik
    initialValues={{ exampleName: "" }}
    name={"exampleForm"}
    onSubmit={handleSubmit}
    validationSchema={validations}
  >
    <Form id={"exampleForm"}>
      <Input {...props} name={"exampleName"} />
    </Form>
  </Formik>
);

const Default = Template.bind({});
Default.args = {
  alertType: "low",
  disabled: false,
  placeholder: "Example placeholder",
  type: "text",
  variant: "solid",
};

export { Default };
export default config;
