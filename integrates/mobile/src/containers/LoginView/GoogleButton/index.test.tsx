import { fireEvent, render, screen } from "@testing-library/react-native";
import React from "react";
import { I18nextProvider } from "react-i18next";

import { GoogleButton } from ".";
import { i18next } from "../../../utils/translations/translate";

describe("GoogleButton", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof GoogleButton).toBe("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    render(
      <I18nextProvider i18n={i18next}>
        <GoogleButton disabled={true} onPress={jest.fn()} />
      </I18nextProvider>
    );

    expect(screen.getByText(/google/iu)).toBeDefined();
  });

  it("should execute callbacks", (): void => {
    expect.hasAssertions();

    const performAuth: jest.Mock = jest.fn();
    render(
      <I18nextProvider i18n={i18next}>
        <GoogleButton disabled={false} onPress={performAuth} />
      </I18nextProvider>
    );
    const googleButton = screen.getByText(/google/iu);

    expect(googleButton).toBeDefined();

    fireEvent(googleButton, "onPress");

    expect(performAuth).toHaveBeenCalledTimes(1);
  });
});
