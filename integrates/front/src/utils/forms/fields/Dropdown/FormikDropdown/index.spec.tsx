import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { Field, Form, Formik } from "formik";
import React from "react";
import { object, string } from "yup";

import { FormikDropdown } from ".";

describe("Dropdown Field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FormikDropdown).toStrictEqual("function");
  });

  it("should render dropdown component", (): void => {
    expect.hasAssertions();

    const dropdownTestSchema = object().shape({
      dropdownTest: string().required(),
    });

    const wrapper: ReactWrapper = mount(
      <Formik
        initialValues={{ dropdownTest: "" }}
        onSubmit={jest.fn()}
        validationSchema={dropdownTestSchema}
      >
        <Form name={""}>
          <Field component={FormikDropdown} name={"dropdownTest"} type={"text"}>
            <option value={""} />
            <option value={"test"}>{"Test"}</option>
          </Field>
        </Form>
      </Formik>
    );

    const options: ReactWrapper = wrapper.find("option");

    expect(options).toHaveLength(2);
  });
});
