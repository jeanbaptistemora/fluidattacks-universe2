import { Field } from "redux-form";
import { FormControl } from "react-bootstrap";
import { GenericForm } from "../../../../scenes/Dashboard/components/GenericForm";
import { Provider } from "react-redux";
import React from "react";
import { TextArea } from "./index";
import { required } from "../../../validations";
import store from "../../../../store";
import { ReactWrapper, mount } from "enzyme";

describe("TextArea Field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof TextArea).toStrictEqual("function");
  });

  it("should render textarea component", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <GenericForm name={""} onSubmit={jest.fn()}>
          <Field
            component={TextArea}
            id={"test"}
            name={"textAreaTest"}
            validate={[required]}
            withCount={false}
          />
        </GenericForm>
      </Provider>
    );

    expect(wrapper.find(FormControl).props().id).toBe("test");
  });
});
