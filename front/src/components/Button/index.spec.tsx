import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import * as React from "react";
import { Button } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("Button", () => {

  it("should return a fuction", () => {
    expect(typeof (Button))
      .toEqual("function");
  });

  it("should render a button", () => {
    const wrapper: ShallowWrapper = shallow(
      <Button
        bsStyle="primary"
        onClick={functionMock}
      >
        Test
      </Button>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
