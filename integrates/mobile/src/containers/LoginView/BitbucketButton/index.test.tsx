import { fireEvent, render, screen } from "@testing-library/react-native";
import React from "react";
import { I18nextProvider } from "react-i18next";

import { BitbucketButton } from ".";
import { i18next } from "../../../utils/translations/translate";

describe("BitbucketButton", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof BitbucketButton).toBe("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    render(
      <I18nextProvider i18n={i18next}>
        <BitbucketButton disabled={true} onPress={jest.fn()} />
      </I18nextProvider>
    );

    expect(screen.getByText(/bitbucket/iu)).toBeDefined();
  });

  it("should execute callbacks", (): void => {
    expect.hasAssertions();

    const performAuth: jest.Mock = jest.fn();
    render(
      <I18nextProvider i18n={i18next}>
        <BitbucketButton disabled={false} onPress={performAuth} />
      </I18nextProvider>
    );
    const bitbucketButton = screen.getByText(/bitbucket/iu);

    expect(bitbucketButton).toBeDefined();

    fireEvent(bitbucketButton, "onPress");

    expect(performAuth).toHaveBeenCalledTimes(1);
  });
});
