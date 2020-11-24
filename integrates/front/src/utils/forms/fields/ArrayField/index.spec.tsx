import { ArrayField } from ".";
import { ArrayWrapper } from "./wrapper";
import { Field } from "redux-form";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { Provider } from "react-redux";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { Text } from "../Text";
import { mount } from "enzyme";
import store from "store";

describe("Array field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ArrayField).toStrictEqual("function");
  });

  it("should add and remove fields", (): void => {
    expect.hasAssertions();

    const handleSubmit: jest.Mock = jest.fn();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <GenericForm
          initialValues={{ names: [{}] }}
          name={"test"}
          onSubmit={handleSubmit}
        >
          <ArrayField name={"names"}>
            {(fieldName: string): JSX.Element => (
              <Field component={Text} name={fieldName} type={"text"} />
            )}
          </ArrayField>
          <button id={"submit"} type={"submit"} />
        </GenericForm>
      </Provider>
    );

    expect(wrapper).toHaveLength(1);

    expect(wrapper.find(ArrayWrapper).find("input")).toHaveLength(1);

    const addButton: ReactWrapper = wrapper.find(".glyphicon-plus");

    expect(addButton).toHaveLength(1);

    expect(wrapper.find(".glyphicon-trash")).toHaveLength(0);

    addButton.simulate("click");

    expect(wrapper.find(ArrayWrapper).find("input")).toHaveLength(2);

    const removeButton: ReactWrapper = wrapper.find(".glyphicon-trash");

    expect(removeButton).toHaveLength(1);

    removeButton.simulate("click");

    expect(wrapper.find(ArrayWrapper).find("input")).toHaveLength(1);
  });
});
