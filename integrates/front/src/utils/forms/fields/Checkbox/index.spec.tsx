import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { Field, Form, Formik } from "formik";
import React from "react";
import { object, string } from "yup";

import { FormikCheckbox } from ".";

const FormikCheckboxSchema = object().shape({
  textTest: string().required(),
});

describe("Checkbox Field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FormikCheckbox).toStrictEqual("function");
  });

  it("should render checkbox component", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Formik initialValues={{ checkboxTest: false }} onSubmit={jest.fn()}>
        <Form name={""}>
          <Field
            component={FormikCheckbox}
            name={"checkboxTest"}
            validationSchema={FormikCheckboxSchema}
          />
        </Form>
      </Formik>
    );

    expect(wrapper.find("Checkbox").first().props().name).toBe("checkboxTest");
  });
});
