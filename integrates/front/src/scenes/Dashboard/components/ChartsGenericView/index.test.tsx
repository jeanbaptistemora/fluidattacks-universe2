import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, waitFor } from "@testing-library/react";
import React from "react";

import { SUBSCRIPTIONS_TO_ENTITY_REPORT } from "./queries";

import { ChartsView } from "scenes/Dashboard/components/ChartsGenericView";

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
    expect(typeof ChartsView).toBe("function");
  });

  it("should render a component and number of graphics of entity", async (): Promise<void> => {
    expect.hasAssertions();

    const groupGraphics: number = 42;
    const organizationAndPortfolioGraphics: number = 47;

    const { container, rerender } = render(
      <MockedProvider addTypename={true} mocks={[mocks]}>
        <ChartsView
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
        <ChartsView
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
        <ChartsView
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
