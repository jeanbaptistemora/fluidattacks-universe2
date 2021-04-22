import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { Field, Form, Formik } from "formik";
import React from "react";
import { object, string } from "yup";

import { FormikTextArea } from ".";

describe("TextArea Field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FormikTextArea).toStrictEqual("function");
  });

  it("should render textarea component", (): void => {
    expect.hasAssertions();

    const textAreaTestSchema = object().shape({
      dropdownTest: string().required(),
    });

    const wrapper: ReactWrapper = mount(
      <Formik
        initialValues={{ textAreaTest: "" }}
        onSubmit={jest.fn()}
        validationSchema={textAreaTestSchema}
      >
        <Form name={""}>
          <Field
            component={FormikTextArea}
            id={"test"}
            name={"textAreaTest"}
            withCount={false}
          />
        </Form>
      </Formik>
    );

    expect(wrapper.find("textarea").props().id).toBe("test");
  });
});
