import { render, screen } from "@testing-library/react";
import _ from "lodash";
import React from "react";

import { SeverityTile } from "./tile";

import { userInteractionBgColor, userInteractionOptions } from "../utils";

describe("SeverityTile", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof SeverityTile).toStrictEqual("function");
  });

  it("should render a tile", (): void => {
    expect.hasAssertions();

    const userInteraction: string = "0.85";
    render(
      <SeverityTile
        color={userInteractionBgColor[userInteraction]}
        name={"userInteraction"}
        value={userInteraction}
        valueText={userInteractionOptions[userInteraction]}
      />
    );

    expect(
      screen.queryByText(_.capitalize(userInteractionOptions[userInteraction]))
    ).toBeInTheDocument();
    expect(screen.queryByText(userInteraction)).toBeInTheDocument();
  });
});
