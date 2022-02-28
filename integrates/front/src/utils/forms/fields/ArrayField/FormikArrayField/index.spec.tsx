import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { Field, Form, Formik } from "formik";
import React from "react";

import { FormikArrayField } from ".";
import { FormikText } from "utils/forms/fields";

describe("Array field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FormikArrayField).toStrictEqual("function");
  });

  it("should add and remove fields", (): void => {
    expect.hasAssertions();

    const handleSubmit: jest.Mock = jest.fn();

    const wrapper: ReactWrapper = mount(
      <Formik
        initialValues={{ names: [""] }}
        name={"test"}
        onSubmit={handleSubmit}
      >
        {(): JSX.Element => (
          <Form>
            <FormikArrayField
              allowEmpty={false}
              initialValue={""}
              name={"names"}
            >
              {(fieldName: string): JSX.Element => (
                <Field component={FormikText} name={fieldName} type={"text"} />
              )}
            </FormikArrayField>
            <button id={"submit"} type={"submit"} />
          </Form>
        )}
      </Formik>
    );

    expect(wrapper).toHaveLength(1);

    expect(wrapper.find(FormikArrayField).find("input")).toHaveLength(1);

    const addButton: ReactWrapper = wrapper.find(".fa-plus");

    expect(addButton).toHaveLength(1);

    expect(wrapper.find(".fa-trash-can")).toHaveLength(0);

    addButton.simulate("click");
    wrapper.update();

    expect(wrapper.find(FormikArrayField).find("input")).toHaveLength(2);

    const removeButton: ReactWrapper = wrapper.find(".fa-trash-can");

    expect(removeButton).toHaveLength(1);

    removeButton.simulate("click");
    wrapper.update();

    expect(wrapper.find(FormikArrayField).find("input")).toHaveLength(1);
  });
});
