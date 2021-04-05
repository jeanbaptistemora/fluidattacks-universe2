import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { Provider } from "react-redux";
import { Field } from "redux-form";

import { TextArea } from ".";
import { GenericForm } from "../../../../scenes/Dashboard/components/GenericForm";
import store from "../../../../store";
import { required } from "../../../validations";

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

    expect(wrapper.find("textarea").props().id).toBe("test");
  });
});
