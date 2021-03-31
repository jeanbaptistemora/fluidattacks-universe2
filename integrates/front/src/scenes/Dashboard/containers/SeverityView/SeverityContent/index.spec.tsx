import React from "react";
import type { ReactWrapper } from "enzyme";
import { SeverityTile } from "./tile";
import { mount } from "enzyme";
import { useTranslation } from "react-i18next";
import { userInteractionBgColor, userInteractionOptions } from "../utils";

describe("SeverityTile", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof SeverityTile).toStrictEqual("function");
  });

  it("should render a tile", (): void => {
    expect.hasAssertions();

    const { t } = useTranslation();
    const userInteraction: string = "0.85";
    const wrapper: ReactWrapper = mount(
      <SeverityTile
        color={userInteractionBgColor[userInteraction]}
        name={"userInteraction"}
        value={userInteraction}
        valueText={t(userInteractionOptions[userInteraction])}
      />
    );

    expect(wrapper).toHaveLength(1);
  });
});
