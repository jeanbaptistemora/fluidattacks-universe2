import { mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import React from "react";
import { Provider } from "react-redux";
import { Field } from "redux-form";
import { GenericForm } from "../../scenes/Dashboard/components/GenericForm";
import store from "../../store";
import { required } from "../validations";
import {
  dateField, dropdownField, fileInputField, tagInputField, textAreaField,
} from "./fields";

describe("Form fields", () => {

  it("should return a dateField function", () => {
    expect(typeof (dateField))
      .toEqual("function");
  });

  it("should return a dropdownField function", () => {
    expect(typeof (dropdownField))
      .toEqual("function");
  });

  it("should return a fileInputField function", () => {
    expect(typeof (fileInputField))
      .toEqual("function");
  });

  it("should return a textAreaField function", () => {
    expect(typeof (textAreaField))
      .toEqual("function");
  });

  it("should return a tagInputField function", () => {
    expect(typeof (tagInputField))
      .toEqual("function");
  });

  it("should render dropdownField component", () => {
    const wrapper: ShallowWrapper = shallow(
      <Field
        name="dropdownTest"
        component={dropdownField}
        type="text"
        validate={[required]}
      >
        <option value="" />
        <option value="test">Test</option>
      </Field>,
    );
    expect(wrapper.find("dropdownTest"))
      .toBeTruthy();
  });

  it("should render fileInputField component", () => {
    const wrapper: ShallowWrapper = shallow(
      <Field
        name="fileInputTest"
        component={fileInputField}
        validate={[required]}
      />,
    );
    expect(wrapper.find("fileInputTest"))
      .toBeTruthy();
  });

  it("should render textAreaField component", () => {
    const wrapper: ShallowWrapper = shallow(
      <Field
        name="textAreaTest"
        withCount={false}
        component={textAreaField}
        validate={[required]}
      />,
    );
    expect(wrapper.find("textAreaTest"))
      .toBeTruthy();
  });

  it("should render dateField component", () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <GenericForm
          name=""
          onSubmit={jest.fn()}
        >
          <Field
            name="dateTest"
            component={dateField}
            validate={[required]}
          />
        </GenericForm>
      </Provider>,
    );
    expect(wrapper.find("dateTest"))
      .toBeTruthy();
  });

  it("should render tagInputField component", () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <GenericForm name="" onSubmit={jest.fn()}>
          <Field
            name="tagInputTest"
            component={tagInputField}
            type="text"
          />
        </GenericForm>
      </Provider>,
    );

    expect(wrapper.find("tagInputTest"))
      .toBeTruthy();
  });
});
