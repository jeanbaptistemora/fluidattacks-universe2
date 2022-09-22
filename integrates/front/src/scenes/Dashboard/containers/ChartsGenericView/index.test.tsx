/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, waitFor } from "@testing-library/react";
import React from "react";

import { SUBSCRIPTIONS_TO_ENTITY_REPORT } from "./queries";

import { ChartsGenericView } from "scenes/Dashboard/containers/ChartsGenericView";
import { ChartsChangedOrderView } from "scenes/Dashboard/containers/ChartsGenericView/newOrderIndex";

describe("ChartsGenericView", (): void => {
  const mocks: MockedResponse = {
    request: {
      query: SUBSCRIPTIONS_TO_ENTITY_REPORT,
    },
    result: {
      data: {
        me: {
          __typename: "Me",
          subscriptionsToEntityReport: [],
          userEmail: "",
        },
      },
    },
  };

  it("should return an function", (): void => {
    expect.hasAssertions();
    expect(typeof ChartsGenericView).toBe("function");
  });

  it("should return an function for changed order", (): void => {
    expect.hasAssertions();
    expect(typeof ChartsChangedOrderView).toBe("function");
  });

  it("should render a component and number of graphics of entity", async (): Promise<void> => {
    expect.hasAssertions();

    const groupGraphics: number = 41;
    const organizationAndPortfolioGraphics: number = 46;

    const { container, rerender } = render(
      <MockedProvider addTypename={true} mocks={[mocks]}>
        <ChartsGenericView
          bgChange={false}
          entity={"organization"}
          reportMode={false}
          subject={"subject"}
        />
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(container.getElementsByClassName("frame")).toHaveLength(
        organizationAndPortfolioGraphics
      );
    });

    rerender(
      <MockedProvider addTypename={true} mocks={[mocks]}>
        <ChartsGenericView
          bgChange={false}
          entity={"group"}
          reportMode={false}
          subject={"subject"}
        />
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(container.getElementsByClassName("frame")).toHaveLength(
        groupGraphics
      );
    });

    rerender(
      <MockedProvider addTypename={true} mocks={[mocks]}>
        <ChartsGenericView
          bgChange={false}
          entity={"portfolio"}
          reportMode={false}
          subject={"subject"}
        />
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(container.getElementsByClassName("frame")).toHaveLength(
        organizationAndPortfolioGraphics
      );
    });
  });

  it("should render a component and number of graphics of entity for changed order", async (): Promise<void> => {
    expect.hasAssertions();

    const groupGraphics: number = 41;
    const organizationAndPortfolioGraphics: number = 46;

    const { container, rerender } = render(
      <MockedProvider addTypename={true} mocks={[mocks]}>
        <ChartsChangedOrderView
          bgChange={false}
          entity={"organization"}
          reportMode={false}
          subject={"subject"}
        />
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(container.getElementsByClassName("frame")).toHaveLength(
        organizationAndPortfolioGraphics
      );
    });

    rerender(
      <MockedProvider addTypename={true} mocks={[mocks]}>
        <ChartsChangedOrderView
          bgChange={false}
          entity={"group"}
          reportMode={false}
          subject={"subject"}
        />
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(container.getElementsByClassName("frame")).toHaveLength(
        groupGraphics
      );
    });

    rerender(
      <MockedProvider addTypename={true} mocks={[mocks]}>
        <ChartsChangedOrderView
          bgChange={false}
          entity={"portfolio"}
          reportMode={false}
          subject={"subject"}
        />
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(container.getElementsByClassName("frame")).toHaveLength(
        organizationAndPortfolioGraphics
      );
    });
  });
});
