import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { Field, Form, Formik } from "formik";
import React from "react";
import PhoneInput from "react-phone-input-2";
import { object, string } from "yup";

import { FormikPhoneNumber } from "utils/forms/fields/PhoneNumber/FormikPhoneNumber";

const FormikPhoneNumberSchema = object().shape({
  phoneTest: string().required(),
});

describe("PhoneNumber Field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FormikPhoneNumber).toStrictEqual("function");
  });

  it("should render phonenumber component", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Formik
        initialValues={{ phoneTest: "" }}
        onSubmit={jest.fn()}
        validationSchema={FormikPhoneNumberSchema}
      >
        <Form name={""}>
          <Field
            component={FormikPhoneNumber}
            id={"test"}
            name={"phoneTest"}
            type={"text"}
          />
        </Form>
      </Formik>
    );

    expect(wrapper.find(PhoneInput).props().country).toBe("co");
  });
});
