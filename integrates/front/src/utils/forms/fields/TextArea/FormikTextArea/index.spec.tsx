import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { Field, Form, Formik } from "formik";
import React from "react";

import { FormikTextArea } from ".";
import { required } from "../../../../validations";

describe("TextArea Field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FormikTextArea).toStrictEqual("function");
  });

  it("should render textarea component", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Formik initialValues={{ textAreaTest: "" }} onSubmit={jest.fn()}>
        <Form name={""}>
          <Field
            component={FormikTextArea}
            id={"test"}
            name={"textAreaTest"}
            validate={required}
            withCount={false}
          />
        </Form>
      </Formik>
    );

    expect(wrapper.find("textarea").props().id).toBe("test");
  });
});
