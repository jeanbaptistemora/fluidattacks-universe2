import type { ReactWrapper, ShallowWrapper } from "enzyme";
import { mount, shallow } from "enzyme";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback } from "react";
import { act } from "react-dom/test-utils";
import { MemoryRouter, useHistory } from "react-router-dom";

import { useWindowSize } from "./useWindowSize";

import { useStoredState, useTabTracking } from "utils/hooks";

describe("Custom utility hooks", (): void => {
  describe("useStoredState", (): void => {
    const TestComponent: React.FC = (): JSX.Element => {
      const [message, setMessage] = useStoredState("message", "fallback");
      const [sort, setSort] = useStoredState("sortOrder", { order: "asc" });

      const handleClick = useCallback((): void => {
        setMessage("Hello world");
        setSort({ order: "none" });
      }, [setMessage, setSort]);

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

      const wrapper: ShallowWrapper = shallow(<TestComponent />);

      expect(wrapper.find("p").at(0).text()).toStrictEqual("fallback");
    });

    it("should load from storage", (): void => {
      expect.hasAssertions();

      sessionStorage.setItem("message", JSON.stringify("stored"));
      sessionStorage.setItem("sortOrder", JSON.stringify({ order: "dsc" }));
      const wrapper: ShallowWrapper = shallow(<TestComponent />);

      expect(wrapper.find("p").at(0).text()).toStrictEqual("stored");
      expect(wrapper.find("p").at(1).text()).toStrictEqual("dsc");
    });

    it("should store state", (): void => {
      expect.hasAssertions();

      const wrapper: ShallowWrapper = shallow(<TestComponent />);

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

  describe("useTabTracking", (): void => {
    // eslint-disable-next-line react/no-multi-comp
    const TestComponent: React.FC = (): JSX.Element => {
      const { push } = useHistory();
      useTabTracking("Group");

      const handleClick: () => void = useCallback((): void => {
        push("/groups/grp2/scope");
      }, [push]);

      return <button onClick={handleClick} />;
    };

    it("should return a function", (): void => {
      expect.hasAssertions();
      expect(typeof useTabTracking).toStrictEqual("function");
    });

    it("should trigger on route change", (): void => {
      expect.hasAssertions();

      const trackMock: jest.SpyInstance = jest.spyOn(mixpanel, "track");

      const wrapper: ReactWrapper = mount(
        <MemoryRouter initialEntries={["/groups/grp1/analytics"]}>
          <TestComponent />
        </MemoryRouter>
      );

      expect(trackMock).toHaveBeenCalledWith("GroupAnalytics", { id: "grp1" });

      act((): void => {
        wrapper.find("button").simulate("click");
      });

      expect(trackMock).toHaveBeenCalledWith("GroupScope", { id: "grp2" });
      expect(trackMock).toHaveBeenCalledTimes(2);

      trackMock.mockReset();
    });
  });

  describe("useWindowSize", (): void => {
    // eslint-disable-next-line react/no-multi-comp
    const TestComponent: React.FC = (): JSX.Element => {
      const { height, width } = useWindowSize();

      return (
        <React.Fragment>
          <p>{height}</p>
          <p>{width}</p>
        </React.Fragment>
      );
    };

    it("should return a function", (): void => {
      expect.hasAssertions();
      expect(typeof useWindowSize).toStrictEqual("function");
    });

    it("should trigger on size change", (): void => {
      expect.hasAssertions();

      const wrapper: ReactWrapper = mount(<TestComponent />);

      expect(wrapper.find("p").at(0).text()).toStrictEqual("768");
      expect(wrapper.find("p").at(1).text()).toStrictEqual("1024");

      // eslint-disable-next-line fp/no-mutating-methods
      Object.defineProperty(window, "innerHeight", { value: 900 });
      // eslint-disable-next-line fp/no-mutating-methods
      Object.defineProperty(window, "innerWidth", { value: 1600 });
      act((): void => {
        window.dispatchEvent(new Event("resize"));
      });

      expect(wrapper.find("p").at(0).text()).toStrictEqual("900");
      expect(wrapper.find("p").at(1).text()).toStrictEqual("1600");
    });
  });
});
