import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import * as React from "react";
import { Provider } from "react-redux";
import store from "../../../../store";
import { addFilesModal as AddFilesModal } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("Add Files modal", () => {

  const wrapper: ShallowWrapper = shallow(
    <Provider store={store}>
      <AddFilesModal
        isOpen={true}
        onClose={functionMock}
        onSubmit={functionMock}
        showUploadProgress={true}
        uploadProgress={10}
      />
    </Provider>,
  );

  it("should return a function", () => {
    expect(typeof (AddFilesModal))
      .toEqual("function");
  });

  it("should render", () => {
    expect(wrapper)
      .toHaveLength(1);
  });
});
