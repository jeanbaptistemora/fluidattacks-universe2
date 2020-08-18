import React from "react";
import { act } from "react-dom/test-utils";
import { useStoredState } from ".";
import { ShallowWrapper, shallow } from "enzyme";

describe("Custom utility hooks", (): void => {
  describe("useStoredState", (): void => {
    const TestComponent: React.FC = (): JSX.Element => {
      const [message, setMessage] = useStoredState("message", "fallback");
      const [sort, setSort] = useStoredState("sortOrder", { order: "asc" });

      function handleClick(): void {
        setMessage("Hello world");
        setSort({ order: "none" });
      }

      return (
        <React.Fragment>
          <p>{message}</p>
          <p>{sort.order}</p>
          <button onClick={handleClick} />
        </React.Fragment>
      );
    };

    it("should return a function", (): void => {
      expect.hasAssertions();
      expect(typeof useStoredState).toStrictEqual("function");
    });

    it("should render with fallback value", (): void => {
      expect.hasAssertions();

      const wrapper: ShallowWrapper = shallow(
        React.createElement(TestComponent)
      );

      expect(wrapper.find("p").at(0).text()).toStrictEqual("fallback");
    });

    it("should load from storage", (): void => {
      expect.hasAssertions();

      sessionStorage.setItem("message", JSON.stringify("stored"));
      sessionStorage.setItem("sortOrder", JSON.stringify({ order: "dsc" }));
      const wrapper: ShallowWrapper = shallow(
        React.createElement(TestComponent)
      );

      expect(wrapper.find("p").at(0).text()).toStrictEqual("stored");
      expect(wrapper.find("p").at(1).text()).toStrictEqual("dsc");
    });

    it("should store state", (): void => {
      expect.hasAssertions();

      const wrapper: ShallowWrapper = shallow(
        React.createElement(TestComponent)
      );

      act((): void => {
        wrapper.find("button").simulate("click");
      });

      expect(wrapper.find("p").at(0).text()).toStrictEqual("Hello world");
      expect(sessionStorage.getItem("message")).toStrictEqual(
        JSON.stringify("Hello world")
      );
      expect(wrapper.find("p").at(1).text()).toStrictEqual("none");
      expect(sessionStorage.getItem("sortOrder")).toStrictEqual(
        JSON.stringify({ order: "none" })
      );
    });
  });
});
