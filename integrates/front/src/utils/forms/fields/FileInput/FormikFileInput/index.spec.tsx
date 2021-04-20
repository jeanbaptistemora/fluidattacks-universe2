import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { Field, Form, Formik } from "formik";
import React from "react";

import { FormGroup } from "styles/styledComponents";
import { FormikFileInput } from "utils/forms/fields/FileInput/FormikFileInput";
import { required } from "utils/validations";

describe("FileInput Field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FormikFileInput).toStrictEqual("function");
  });

  it("should render fileinput component", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Formik initialValues={{ fileInputTest: "" }} onSubmit={jest.fn()}>
        <Form name={""}>
          <Field
            component={FormikFileInput}
            id={"test"}
            name={"fileInputTest"}
            validate={required}
          />
        </Form>
      </Formik>
    );

    expect(wrapper.find(FormGroup).props().id).toBe("test");
  });
});
