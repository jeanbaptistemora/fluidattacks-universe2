import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { Field, Form, Formik } from "formik";
import React from "react";
import { act } from "react-dom/test-utils";
import { WithContext as ReactTagInput } from "react-tag-input";
import waitForExpect from "wait-for-expect";

import { FormikTagInput } from "utils/forms/fields/TagInput/FormikTagInput";

describe("FormikTagInput Field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FormikTagInput).toStrictEqual("function");
  });

  it("should render formiktaginput component", async (): Promise<void> => {
    expect.hasAssertions();

    const MAX_LENGTH_VALUE: number = 30;
    const wrapper: ReactWrapper = mount(
      <Formik
        enableReinitialize={true}
        initialValues={{ tagInputTest: "" }}
        onSubmit={jest.fn()}
      >
        <Form>
          <Field
            component={FormikTagInput}
            name={"tagInputTest"}
            placeholder={""}
            type={"text"}
          />
        </Form>
      </Formik>
    );
    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper.find(ReactTagInput).props().name).toBe("tagInputTest");
        expect(
          wrapper.find({ name: "tagInputTest" }).find("input").first().props()
            .maxLength
        ).toBe(MAX_LENGTH_VALUE);
      });
    });
  });
});
