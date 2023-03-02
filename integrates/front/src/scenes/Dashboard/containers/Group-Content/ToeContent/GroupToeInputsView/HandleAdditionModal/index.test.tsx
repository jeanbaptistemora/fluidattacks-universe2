import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";

import { GET_ROOTS } from "./queries";

import { HandleAdditionModal } from ".";

describe("Handle addition modal", (): void => {
  const refetchDataFn: jest.Mock = jest.fn();
  const handleCloseModal: jest.Mock = jest.fn();
  const queryMock: MockedResponse = {
    request: {
      query: GET_ROOTS,
      variables: { groupName: "groupname" },
    },
    result: {
      data: {
        group: {
          __typename: "Group",
          name: "test",
          roots: [
            {
              __typename: "GitRoot",
              gitEnvironmentUrls: [
                {
                  __typename: "GitEnvironmentUrl",
                  id: "00fbe3579a253b43239954a545dc0536e6c83094",
                  url: "https://app.fluidattacks.com/test",
                  urlType: "URL",
                },
              ],
              id: "4039d098-ffc5-4984-8ed3-eb17bca98e19",
              nickname: "universe",
              state: "ACTIVE",
            },
          ],
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof HandleAdditionModal).toBe("function");
  });

  it("should render modal", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    render(
      <MockedProvider addTypename={false} mocks={[queryMock]}>
        <HandleAdditionModal
          groupName={"groupname"}
          handleCloseModal={handleCloseModal}
          refetchData={refetchDataFn}
        />
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(
        screen.getByText("group.toe.inputs.addModal.title")
      ).toBeInTheDocument();
      expect(screen.getByText("Root")).toBeInTheDocument();
      expect(screen.getByText("Environment url")).toBeInTheDocument();
      expect(
        screen.getByText("group.toe.inputs.addModal.fields.component")
      ).toBeInTheDocument();
      expect(
        screen.getByText("group.toe.inputs.addModal.fields.entryPoint")
      ).toBeInTheDocument();
    });
  });
});
