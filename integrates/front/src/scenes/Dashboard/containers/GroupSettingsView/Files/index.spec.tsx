// Needed to allow lazy updates of test components
/* eslint-disable @typescript-eslint/no-unsafe-return */
import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import wait from "waait";

import type { IFilesProps } from "scenes/Dashboard/containers/GroupSettingsView/Files";
import { Files } from "scenes/Dashboard/containers/GroupSettingsView/Files";
import {
  ADD_FILES_TO_DB_MUTATION,
  DOWNLOAD_FILE_MUTATION,
  GET_FILES,
  REMOVE_FILE_MUTATION,
} from "scenes/Dashboard/containers/GroupSettingsView/queries";
import store from "store";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary = jest.requireActual(
    "../../../../../utils/notifications"
  );

  mockedNotifications.msgError = jest.fn(); // eslint-disable-line fp/no-mutation, jest/prefer-spy-on
  mockedNotifications.msgSuccess = jest.fn(); // eslint-disable-line fp/no-mutation, jest/prefer-spy-on

  return mockedNotifications;
});

describe("Files", (): void => {
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
            environments: "",
            files: JSON.stringify([
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
            ]),
            groupName: "TEST",
            repositories: "",
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
            environments: "",
            files: JSON.stringify([
              {
                description: "Test",
                fileName: "test.zip",
                uploadDate: "2019-03-01 15:21",
                uploader: "unittest@fluidattacks.com",
              },
            ]),
            groupName: "TEST",
            repositories: "",
          },
        },
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Files).toStrictEqual("function");
  });

  // Temporarily disabled until it gets properly refactored to Formik
  // eslint-disable-next-line jest/no-disabled-tests
  it.skip("should add a file", async (): Promise<void> => {
    expect.hasAssertions();

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
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_add_files_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider
          addTypename={false}
          mocks={mocksFiles.concat(mocksMutation)}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Files groupName={mockProps.groupName} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const addButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Add"))
      .at(0);
    addButton.simulate("click", {
      persist: jest.fn(),
    });
    const addFilesModal: ReactWrapper = wrapper.find("addFilesModal");
    const fileInput: ReactWrapper = addFilesModal
      .find({ name: "file" })
      .at(0)
      .find("input");
    fileInput.simulate("change", {
      persist: jest.fn(),
      target: { files: [file], name: "file" },
    });
    const descriptionInput: ReactWrapper = addFilesModal
      .find({ name: "description", type: "text" })
      .at(0)
      .find("textarea");
    descriptionInput.simulate("change", {
      persist: jest.fn(),
      target: { name: "description", value: "Test description" },
    });
    const form: ReactWrapper = addFilesModal.find("Formik").at(0);
    await act(async (): Promise<void> => {
      form.simulate("submit");
      await wait(0);
      wrapper.update();
    });
    await wait(0);

    expect(msgSuccess).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with

    jest.clearAllMocks();
  });

  it("should sort files", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={mocksFiles}>
          <Files groupName={mockProps.groupName} />
        </MockedProvider>
      </Provider>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const firstRowInfo: ReactWrapper = wrapper.find("SimpleRow").at(0);

    expect(firstRowInfo.text()).toStrictEqual("test.zipTest2019-03-01 15:21");

    const fileNameHeader: ReactWrapper = wrapper.find({
      "aria-label": "File sortable",
    });
    fileNameHeader.simulate("click");
    fileNameHeader.simulate("click");
    const firstRowInfo2: ReactWrapper = wrapper.find("SimpleRow").at(0);

    expect(firstRowInfo2.text()).toStrictEqual(
      "shell.exeshell2019-04-24 14:56"
    );

    jest.clearAllMocks();
  });

  it("should remove a file", async (): Promise<void> => {
    expect.hasAssertions();

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
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider
          addTypename={false}
          mocks={mocksFiles.concat(mocksMutation)}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Files groupName={mockProps.groupName} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const fileInfo: ReactWrapper = wrapper
      .find("tr")
      .findWhere((element: ReactWrapper): boolean =>
        element.contains("test.zip")
      )
      .at(0);
    fileInfo.simulate("click");
    const fileOptionsModal: ReactWrapper = wrapper.find("fileOptionsModal");
    const removeButton: ReactWrapper = fileOptionsModal
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Remove"))
      .at(0);
    removeButton.simulate("click");

    const proceedButton: ReactWrapper = wrapper
      .find("ConfirmDialog")
      .find("Button")
      .filterWhere((element: ReactWrapper): boolean =>
        element.contains("Proceed")
      );
    proceedButton.first().simulate("click");

    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(msgSuccess).toHaveBeenCalledTimes(1);

    jest.clearAllMocks();
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
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider
          addTypename={false}
          mocks={mocksFiles.concat(mocksMutation)}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Files groupName={mockProps.groupName} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const fileInfo: ReactWrapper = wrapper
      .find("tr")
      .findWhere((element: ReactWrapper): boolean =>
        element.contains("test.zip")
      )
      .at(0);
    fileInfo.simulate("click");
    const fileOptionsModal: ReactWrapper = wrapper.find("fileOptionsModal");
    const downloadButton: ReactWrapper = fileOptionsModal
      .find("button")
      .findWhere((element: ReactWrapper): boolean =>
        element.contains("Download")
      )
      .at(0);
    downloadButton.simulate("click");
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(open).toHaveBeenCalledWith(
      "https://test.com/file",
      undefined,
      "noopener,noreferrer,"
    );

    jest.clearAllMocks();
  });

  // Temporarily disabled until it gets properly refactored to Formik
  // eslint-disable-next-line jest/no-disabled-tests
  it.skip("should handle errors when adding a file", async (): Promise<void> => {
    expect.hasAssertions();

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
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider
          addTypename={false}
          mocks={mocksFiles.concat(mocksMutation)}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Files groupName={mockProps.groupName} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const addButton = (): ReactWrapper =>
      wrapper
        .find("button")
        .findWhere((element: ReactWrapper): boolean => element.contains("Add"))
        .at(0);
    addButton().simulate("click");
    const addFilesModal = (): ReactWrapper => wrapper.find("addFilesModal");
    const fileInput: ReactWrapper = addFilesModal()
      .find({ name: "file" })
      .at(0)
      .find("input");
    fileInput.simulate("change", { target: { files: [file], name: "file" } });
    const descriptionInput: ReactWrapper = addFilesModal()
      .find({ name: "description", type: "text" })
      .at(0)
      .find("textarea");
    descriptionInput.simulate("change", {
      target: { name: "description", value: "Test description" },
    });
    const form: ReactWrapper = addFilesModal().find("Formik").at(0);
    await act(async (): Promise<void> => {
      form.simulate("submit");
      const delay = 100;
      await wait(delay);
      wrapper.update();
    });

    const TEST_CALLING_TIMES = 3;

    expect(msgError).toHaveBeenCalledTimes(TEST_CALLING_TIMES);

    jest.clearAllMocks();
  });

  // Temporarily disabled until it gets properly refactored to Formik
  // eslint-disable-next-line jest/no-disabled-tests
  it.skip("should handle error when there are repeated files", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_add_files_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={mocksFiles}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Files groupName={mockProps.groupName} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const addButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Add"))
      .at(0);
    addButton.simulate("click");
    const addFilesModal: ReactWrapper = wrapper.find("addFilesModal");
    const file: File = new File([""], "test.zip", { type: "application/zip" });
    const fileInput: ReactWrapper = addFilesModal
      .find({ name: "file" })
      .at(0)
      .find("input");
    fileInput.simulate("change", { target: { files: [file], name: "file" } });
    const descriptionInput: ReactWrapper = addFilesModal
      .find({ name: "description", type: "text" })
      .at(0)
      .find("textarea");
    descriptionInput.simulate("change", {
      target: { name: "description", value: "Test description" },
    });
    const form: ReactWrapper = addFilesModal.find("Formik").at(0);
    await act(async (): Promise<void> => {
      form.simulate("submit");
      await wait(0);
      wrapper.update();
    });
    await wait(0);

    expect(msgError).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with

    jest.clearAllMocks();
  });
});
