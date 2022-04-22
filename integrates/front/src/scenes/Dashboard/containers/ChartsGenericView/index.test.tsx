import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, waitFor } from "@testing-library/react";
import React from "react";

import { SUBSCRIPTIONS_TO_ENTITY_REPORT } from "./queries";

import { ChartsGenericView } from "scenes/Dashboard/containers/ChartsGenericView";

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

  it("should render a component and number of graphics of entity", async (): Promise<void> => {
    expect.hasAssertions();

    const groupGraphics: number = 30;
    const organizationAndPportfolioGraphics: number = 35;

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
        organizationAndPportfolioGraphics
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
        organizationAndPportfolioGraphics
      );
    });
  });
});
