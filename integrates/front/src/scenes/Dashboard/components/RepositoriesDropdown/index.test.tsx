import { render, screen } from "@testing-library/react";
import React from "react";

import { RepositoriesDropdown } from ".";

describe("Dropdown", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof RepositoriesDropdown).toBe("function");
  });

  it("should render a dropdown", (): void => {
    expect.hasAssertions();

    render(
      <RepositoriesDropdown
        availableRepositories={{
          azure: {
            isVisible: true,
            onClick: (): void => undefined,
          },
          gitLab: {
            isVisible: true,
            onClick: (): void => undefined,
          },
        }}
        dropDownText={"Add credential"}
      />
    );

    expect(screen.queryByText("Add credential")).toBeInTheDocument();
    expect(
      screen.queryByText("components.repositoriesDropdown.gitLabButton.text")
    ).toBeInTheDocument();
    expect(
      screen.queryByText("components.repositoriesDropdown.azureButton.text")
    ).toBeInTheDocument();
    expect(
      screen.queryByText("components.repositoriesDropdown.gitHubButton.text")
    ).not.toBeInTheDocument();
    expect(
      screen.queryByText("components.repositoriesDropdown.bitbucketButton.text")
    ).not.toBeInTheDocument();
    expect(
      screen.queryByText("components.repositoriesDropdown.otherButton.text")
    ).not.toBeInTheDocument();
  });
});
