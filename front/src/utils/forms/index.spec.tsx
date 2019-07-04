import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { Field } from "redux-form";
import { required } from "../validations";
import { dropdownField, fileInputField, phoneNumberField, textAreaField, textField } from "./fields";

configure({ adapter: new ReactSixteenAdapter() });

describe("Form fields", () => {
  it("should return a textField function", () => {
    expect(typeof (textField))
      .toEqual("function");
  });

  it("should return a phoneNumberField function", () => {
    expect(typeof (phoneNumberField))
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

  it("should render textField component", () => {
    const wrapper: ShallowWrapper = shallow(
      <Field
        name="textTest"
        component={textField}
        type="text"
        validate={[required]}
      />,
    );
    expect(wrapper.find("textTest"))
      .toBeTruthy();
  });

  it("should render phoneNumberField component", () => {
    const wrapper: ShallowWrapper = shallow(
      <Field
        name="phoneTest"
        component={phoneNumberField}
        type="text"
        validate={[required]}
      />,
    );
    expect(wrapper.find("phoneTest"))
      .toBeTruthy();
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
});
