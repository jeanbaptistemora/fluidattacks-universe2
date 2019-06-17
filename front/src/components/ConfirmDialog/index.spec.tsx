import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import * as React from "react";
import { Provider } from "react-redux";
import store from "../../store/index";
import ConfirmDialog from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("Confirm dialog", () => {

  it("should return an object", () => {
    expect(typeof (ConfirmDialog))
      .toEqual("object");
  });

  it("should render a component", () => {
    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}>
      <ConfirmDialog
        name="confirmTest"
        title="Test"
        onProceed={functionMock}
      />
      </Provider>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
