/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import { Form, Formik } from "formik";
import React from "react";
import { object, string } from "yup";

import type { ICheckboxProps } from "./CustomCheckbox";

import { Checkbox } from ".";
import { Logger } from "utils/logger";

const config: Meta = {
  component: Checkbox,
  title: "components/Checkbox",
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

const Template: Story<ICheckboxProps> = (props): JSX.Element => (
  <Formik
    initialValues={{ exampleName: "" }}
    name={"exampleForm"}
    onSubmit={handleSubmit}
    validationSchema={validations}
  >
    <Form id={"exampleForm"}>
      <Checkbox {...props} />
      &nbsp;{"Example Text"}
    </Form>
  </Formik>
);

const Default = Template.bind({});
Default.args = {
  disabled: true,
};

export { Default };
export default config;
