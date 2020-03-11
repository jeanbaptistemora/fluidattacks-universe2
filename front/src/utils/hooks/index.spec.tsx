import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { useStoredState } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Custom utility hooks", () => {

  describe("useStoredState", () => {

    const testComponent: React.FC = (): JSX.Element => {
      const [message, setMessage] = useStoredState("message", "fallback");
      const [sort, setSort] = useStoredState("sortOrder", { order: "asc" });

      const handleClick: (() => void) = (): void => {
        setMessage("Hello world");
        setSort({ order: "none" });
      };

      return (
        <React.Fragment>
          <p>{message}</p>
          <p>{sort.order}</p>
          <button onClick={handleClick} />
        </React.Fragment>
      );
    };

    it("should return a function", () => {
      expect(typeof useStoredState)
        .toEqual("function");
    });

    it("should render with fallback value", () => {
      const wrapper: ShallowWrapper = shallow(React.createElement(testComponent));

      expect(wrapper.find("p")
        .at(0)
        .text())
        .toEqual("fallback");
    });

    it("should load from storage", () => {
      sessionStorage.setItem("message", "stored");
      sessionStorage.setItem("sortOrder", JSON.stringify({ order: "dsc" }));
      const wrapper: ShallowWrapper = shallow(React.createElement(testComponent));

      expect(wrapper.find("p")
        .at(0)
        .text())
        .toEqual("stored");
      expect(wrapper.find("p")
        .at(1)
        .text())
        .toEqual("dsc");
    });

    it("should store state", () => {
      const wrapper: ShallowWrapper = shallow(React.createElement(testComponent));

      act(() => {
        wrapper.find("button")
          .simulate("click");
      });

      expect(wrapper.find("p")
        .at(0)
        .text())
        .toEqual("Hello world");
      expect(sessionStorage.getItem("message"))
        .toEqual("Hello world");
      expect(wrapper.find("p")
        .at(1)
        .text())
        .toEqual("none");
      expect(sessionStorage.getItem("sortOrder"))
        .toEqual(JSON.stringify({ order: "none" }));
    });
  });
});
