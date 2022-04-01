import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { FileOptionsModal } from "scenes/Dashboard/components/FileOptionsModal";

const functionMock: () => void = (): void => undefined;

describe("Add resources modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FileOptionsModal).toStrictEqual("function");
  });

  it("should render", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <FileOptionsModal
        canRemove={true}
        fileName={""}
        isOpen={true}
        onClose={functionMock}
        onDelete={functionMock}
        onDownload={functionMock}
      />
    );

    expect(
      screen.queryByText("searchFindings.tabResources.modalOptionsTitle")
    ).toBeInTheDocument();
    expect(
      screen.queryByText("searchFindings.tabResources.files.confirm.title")
    ).not.toBeInTheDocument();

    userEvent.click(
      screen.getByRole("button", {
        name: "searchFindings.tabResources.removeRepository",
      })
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabResources.files.confirm.title")
      ).toBeInTheDocument();
    });
  });
});
