import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { Field, Form, Formik } from "formik";
import React from "react";
import { object, string } from "yup";

import { FormikText } from "utils/forms/fields/Text/FormikText";

const FormikTextSchema = object().shape({
  textTest: string().required(),
});

describe("Text Field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Text).toStrictEqual("function");
  });

  it("should render text component", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Formik
        initialValues={{ textTest: "" }}
        onSubmit={jest.fn()}
        validationSchema={FormikTextSchema}
      >
        <Form name={""}>
          <Field
            component={FormikText}
            id={"test"}
            name={"textTest"}
            type={"text"}
          />
        </Form>
      </Formik>
    );

    expect(wrapper.find("input").props().id).toBe("test");
  });
});
