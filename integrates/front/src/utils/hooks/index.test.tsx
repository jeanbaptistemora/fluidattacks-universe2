import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
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
      expect(typeof useStoredState).toBe("function");
    });

    it("should render with fallback value", (): void => {
      expect.hasAssertions();

      render(<TestComponent />);

      expect(screen.queryByText("fallback")).toBeInTheDocument();

      jest.clearAllMocks();
    });

    it("should load from storage", (): void => {
      expect.hasAssertions();

      sessionStorage.setItem("message", JSON.stringify("stored"));
      sessionStorage.setItem("sortOrder", JSON.stringify({ order: "dsc" }));
      render(<TestComponent />);

      expect(screen.queryByText("stored")).toBeInTheDocument();
      expect(screen.queryByText("dsc")).toBeInTheDocument();

      jest.clearAllMocks();
    });

    it("should store state", async (): Promise<void> => {
      expect.hasAssertions();

      render(<TestComponent />);

      expect(screen.queryByRole("button")).toBeInTheDocument();
      expect(screen.queryByText("Hello world")).not.toBeInTheDocument();

      userEvent.click(screen.getByRole("button"));
      await waitFor((): void => {
        expect(screen.queryByText("Hello world")).toBeInTheDocument();
      });

      expect(sessionStorage.getItem("message")).toStrictEqual(
        JSON.stringify("Hello world")
      );
      expect(screen.queryByText("none")).toBeInTheDocument();
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
      expect(typeof useTabTracking).toBe("function");
    });

    it("should trigger on route change", async (): Promise<void> => {
      expect.hasAssertions();

      const trackMock: jest.SpyInstance = jest.spyOn(mixpanel, "track");

      render(
        <MemoryRouter initialEntries={["/groups/grp1/analytics"]}>
          <TestComponent />
        </MemoryRouter>
      );

      expect(trackMock).toHaveBeenCalledWith("GroupAnalytics", { id: "grp1" });
      expect(screen.queryByRole("button")).toBeInTheDocument();

      userEvent.click(screen.getByRole("button"));
      await waitFor((): void => {
        expect(trackMock).toHaveBeenCalledTimes(2);
      });

      expect(trackMock).toHaveBeenCalledWith("GroupScope", { id: "grp2" });

      trackMock.mockReset();
      jest.clearAllMocks();
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
      expect(typeof useWindowSize).toBe("function");
    });

    it("should trigger on size change", async (): Promise<void> => {
      expect.hasAssertions();

      render(<TestComponent />);

      expect(screen.queryByText("768")).toBeInTheDocument();
      expect(screen.queryByText("1024")).toBeInTheDocument();

      // eslint-disable-next-line fp/no-mutating-methods
      Object.defineProperty(window, "innerHeight", { value: 900 });
      // eslint-disable-next-line fp/no-mutating-methods
      Object.defineProperty(window, "innerWidth", { value: 1600 });
      act((): void => {
        window.dispatchEvent(new Event("resize"));
      });

      await waitFor((): void => {
        expect(screen.queryByText("900")).toBeInTheDocument();
      });

      expect(screen.queryByText("1600")).toBeInTheDocument();
    });
  });
});
