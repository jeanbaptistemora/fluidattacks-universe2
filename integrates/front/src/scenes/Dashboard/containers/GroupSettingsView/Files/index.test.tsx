import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { FetchMockStatic } from "fetch-mock";
import { GraphQLError } from "graphql";
import React from "react";

import type { IGetFilesQuery } from "../types";
import type { IFilesProps } from "scenes/Dashboard/containers/GroupSettingsView/Files";
import { Files } from "scenes/Dashboard/containers/GroupSettingsView/Files";
import {
  ADD_FILES_TO_DB_MUTATION,
  DOWNLOAD_FILE_MUTATION,
  GET_FILES,
  REMOVE_FILE_MUTATION,
  SIGN_POST_URL_MUTATION,
} from "scenes/Dashboard/containers/GroupSettingsView/queries";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";

const mockedFetch: FetchMockStatic = fetch as FetchMockStatic & typeof fetch;
mockedFetch.mock("https://mocked.test", {
  body: {},
  status: 200,
});

jest.mock("../../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("Files", (): void => {
  const NUMBER_OF_ROWS: number = 3;
  const mockProps: IFilesProps = {
    groupName: "TEST",
  };

  const mocksFiles: readonly MockedResponse[] = [
    {
      request: {
        query: GET_FILES,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        data: {
          resources: {
            files: [
              {
                description: "Test",
                fileName: "test.zip",
                uploadDate: "2019-03-01 15:21",
                uploader: "unittest@fluidattacks.com",
              },
              {
                description: "shell",
                fileName: "shell.exe",
                uploadDate: "2019-04-24 14:56",
                uploader: "unittest@fluidattacks.com",
              },
            ],
            groupName: "TEST",
          },
        },
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Files).toBe("function");
  });

  it("should add a file", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedFiles: IGetFilesQuery = (
      mocksFiles[0].result as Dictionary<{
        resources: IGetFilesQuery["resources"];
      }>
    ).data;
    const file: File = new File([""], "image.png", { type: "image/png" });
    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: ADD_FILES_TO_DB_MUTATION,
          variables: {
            filesData: JSON.stringify([
              {
                description: "Test description",
                fileName: "image.png",
              },
            ]),
            groupName: "TEST",
          },
        },
        result: { data: { addFilesToDb: { success: true } } },
      },
      {
        request: {
          query: SIGN_POST_URL_MUTATION,
          variables: {
            filesData: JSON.stringify([
              {
                description: "Test description",
                fileName: "image.png",
              },
            ]),
            groupName: "TEST",
          },
        },
        result: {
          data: {
            signPostUrl: {
              success: true,
              url: {
                fields: {
                  awsaccesskeyid: "",
                  key: "",
                  policy: "",
                  signature: "",
                },
                url: "https://mocked.test",
              },
            },
          },
        },
      },
      {
        request: {
          query: GET_FILES,
          variables: {
            groupName: "TEST",
          },
        },
        result: {
          data: {
            resources: {
              files: [
                ...(mockedFiles.resources.files === null
                  ? []
                  : mockedFiles.resources.files),
                {
                  description: "Test description",
                  fileName: "image.png",
                  uploadDate: "",
                  uploader: "",
                },
              ],
              groupName: "TEST",
            },
          },
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_add_files_mutate" },
    ]);
    render(
      <MockedProvider
        addTypename={false}
        mocks={[...mocksFiles, ...mocksMutation]}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <Files groupName={mockProps.groupName} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(NUMBER_OF_ROWS);
    });

    expect(
      screen.queryByText("searchFindings.tabResources.addRepository")
    ).toBeInTheDocument();

    userEvent.click(
      screen.getByText("searchFindings.tabResources.addRepository")
    );

    await waitFor((): void => {
      expect(screen.queryByTestId("file")).toBeInTheDocument();
    });

    expect(screen.getByText("confirmmodal.proceed")).toBeDisabled();

    await waitFor((): void => {
      fireEvent.change(screen.getByTestId("file"), {
        target: { files: [file] },
      });
    });
    userEvent.type(
      screen.getByRole("textbox", { name: "description" }),
      "Test description"
    );
    await waitFor((): void => {
      expect(screen.getByText("confirmmodal.proceed")).not.toBeDisabled();
    });
    userEvent.click(screen.getByText("confirmmodal.proceed"));
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(4);
    });

    jest.clearAllMocks();
  });

  it("should sort files", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MockedProvider addTypename={false} mocks={mocksFiles}>
        <Files groupName={mockProps.groupName} />
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(NUMBER_OF_ROWS);
    });

    expect(screen.queryAllByRole("row")[1].textContent).toStrictEqual(
      "test.zipTest2019-03-01 15:21"
    );

    userEvent.click(
      screen.getByRole("columnheader", {
        name: "searchFindings.filesTable.file sortable",
      })
    );
    userEvent.click(
      screen.getByRole("columnheader", {
        name: "searchFindings.filesTable.file sort desc",
      })
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")[1].textContent).toStrictEqual(
        "shell.exeshell2019-04-24 14:56"
      );
    });

    expect(
      screen.queryByRole("columnheader", {
        name: "searchFindings.filesTable.file sort desc",
      })
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("columnheader", {
        name: "searchFindings.filesTable.file sort asc",
      })
    ).toBeInTheDocument();

    jest.clearAllMocks();
  });

  it("should remove a file", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: REMOVE_FILE_MUTATION,
          variables: {
            filesData: JSON.stringify({
              fileName: "test.zip",
            }),
            groupName: "TEST",
          },
        },
        result: { data: { removeFiles: { success: true } } },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_remove_files_mutate" },
    ]);
    render(
      <MockedProvider
        addTypename={false}
        mocks={mocksFiles.concat(mocksMutation)}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <Files groupName={mockProps.groupName} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(NUMBER_OF_ROWS);
    });

    expect(screen.queryByText("test.zip")).toBeInTheDocument();

    userEvent.click(screen.getByText("test.zip"));
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabResources.modalOptionsTitle")
      ).toBeInTheDocument();
    });
    userEvent.click(
      screen.getByText("searchFindings.tabResources.removeRepository")
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabResources.files.confirm.title")
      ).toBeInTheDocument();
    });
    userEvent.click(screen.getByText("confirmmodal.proceed"));
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledTimes(1);
    });
  });

  it("should download a file", async (): Promise<void> => {
    expect.hasAssertions();

    const open: jest.Mock = jest.fn();
    open.mockReturnValue({ opener: "" });
    window.open = open; // eslint-disable-line fp/no-mutation
    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: DOWNLOAD_FILE_MUTATION,
          variables: {
            filesData: JSON.stringify("test.zip"),
            groupName: "TEST",
          },
        },
        result: {
          data: {
            downloadFile: { success: true, url: "https://test.com/file" },
          },
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_remove_files_mutate" },
    ]);
    render(
      <MockedProvider
        addTypename={false}
        mocks={mocksFiles.concat(mocksMutation)}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <Files groupName={mockProps.groupName} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(NUMBER_OF_ROWS);
    });

    expect(screen.queryByText("test.zip")).toBeInTheDocument();

    userEvent.click(screen.getByText("test.zip"));
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabResources.modalOptionsTitle")
      ).toBeInTheDocument();
    });
    userEvent.click(screen.getByText("searchFindings.tabResources.download"));
    await waitFor((): void => {
      expect(open).toHaveBeenCalledWith(
        "https://test.com/file",
        undefined,
        "noopener,noreferrer,"
      );
    });
  });

  it("should handle errors when adding a file", async (): Promise<void> => {
    expect.hasAssertions();

    const file: File = new File([""], "image.png", { type: "image/png" });
    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: SIGN_POST_URL_MUTATION,
          variables: {
            filesData: JSON.stringify([
              {
                description: "Test description",
                fileName: "image.png",
              },
            ]),
            groupName: "TEST",
          },
        },
        result: {
          data: {
            signPostUrl: {
              success: true,
              url: {
                fields: {
                  awsaccesskeyid: "",
                  key: "",
                  policy: "",
                  signature: "",
                },
                url: "https://mocked.test",
              },
            },
          },
        },
      },
      {
        request: {
          query: ADD_FILES_TO_DB_MUTATION,
          variables: {
            filesData: JSON.stringify([
              {
                description: "Test description",
                fileName: "image.png",
              },
            ]),
            groupName: "TEST",
          },
        },
        result: {
          errors: [
            new GraphQLError("Access denied"),
            new GraphQLError("Exception - Invalid field in form"),
            new GraphQLError("Exception - Invalid characters"),
          ],
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_add_files_mutate" },
    ]);
    render(
      <MockedProvider
        addTypename={false}
        mocks={mocksFiles.concat(mocksMutation)}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <Files groupName={mockProps.groupName} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(NUMBER_OF_ROWS);
    });

    expect(
      screen.queryByText("searchFindings.tabResources.addRepository")
    ).toBeInTheDocument();

    userEvent.click(
      screen.getByText("searchFindings.tabResources.addRepository")
    );

    await waitFor((): void => {
      expect(screen.queryByTestId("file")).toBeInTheDocument();
    });

    expect(screen.getByText("confirmmodal.proceed")).toBeDisabled();

    await waitFor((): void => {
      fireEvent.change(screen.getByTestId("file"), {
        target: { files: [file] },
      });
    });
    userEvent.type(
      screen.getByRole("textbox", { name: "description" }),
      "Test description"
    );
    await waitFor((): void => {
      expect(screen.getByText("confirmmodal.proceed")).not.toBeDisabled();
    });
    userEvent.click(screen.getByText("confirmmodal.proceed"));
    const TEST_CALLING_TIMES = 3;

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(TEST_CALLING_TIMES);
    });

    jest.clearAllMocks();
  });

  it("should handle error when there are repeated files", async (): Promise<void> => {
    expect.hasAssertions();

    const file: File = new File([""], "test.zip", { type: "application/zip" });
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_add_files_mutate" },
    ]);
    render(
      <MockedProvider addTypename={false} mocks={mocksFiles}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <Files groupName={mockProps.groupName} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(NUMBER_OF_ROWS);
    });

    expect(
      screen.queryByText("searchFindings.tabResources.addRepository")
    ).toBeInTheDocument();

    userEvent.click(
      screen.getByText("searchFindings.tabResources.addRepository")
    );

    await waitFor((): void => {
      expect(screen.queryByTestId("file")).toBeInTheDocument();
    });

    expect(screen.getByText("confirmmodal.proceed")).toBeDisabled();

    await waitFor((): void => {
      fireEvent.change(screen.getByTestId("file"), {
        target: { files: [file] },
      });
    });
    userEvent.type(
      screen.getByRole("textbox", { name: "description" }),
      "Test description"
    );
    await waitFor((): void => {
      expect(screen.getByText("confirmmodal.proceed")).not.toBeDisabled();
    });
    userEvent.click(screen.getByText("confirmmodal.proceed"));

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(
        "searchFindings.tabResources.repeatedItem"
      );
    });
    jest.clearAllMocks();
  });
});
