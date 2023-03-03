import { render, screen } from "@testing-library/react";
import React from "react";

import { RepositoriesDropdown } from ".";
import { gitLabIcon } from "resources";

describe("Card", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof RepositoriesDropdown).toBe("function");
  });

  it("should render a dropdown", (): void => {
    expect.hasAssertions();

    render(
      <RepositoriesDropdown
        availableRepositories={[
          {
            icon: gitLabIcon,
            id: "gitlabButton",
            isVisible: true,
            onClick: (): void => undefined,
            text: "GitLab",
          },
        ]}
        dropDownText={"Add credentials"}
      />
    );

    expect(screen.queryByText("Add credentials")).toBeInTheDocument();
    expect(screen.queryByText("GitLab")).toBeInTheDocument();
  });
});
