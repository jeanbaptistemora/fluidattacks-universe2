import { PureAbility } from "@casl/ability";
import { render, screen } from "@testing-library/react";
import React from "react";

import { FindingActions } from "scenes/Dashboard/components/FindingActions";
import { authzPermissionsContext } from "utils/authz/config";

describe("FindingActions", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FindingActions).toBe("function");
  });

  it("should render no actions", (): void => {
    expect.hasAssertions();

    render(
      <FindingActions
        hasSubmission={false}
        hasVulns={false}
        isDraft={false}
        loading={false}
        onApprove={jest.fn()}
        onDelete={jest.fn()}
        onReject={jest.fn()}
        onSubmit={jest.fn()}
      />
    );

    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("should render hacker finding actions", (): void => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_remove_finding_mutate" },
    ]);
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <FindingActions
          hasSubmission={true}
          hasVulns={false}
          isDraft={true}
          loading={false}
          onApprove={jest.fn()}
          onDelete={jest.fn()}
          onReject={jest.fn()}
          onSubmit={jest.fn()}
        />
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryByRole("button")).toBeInTheDocument();
  });

  it("should render author draft actions", (): void => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_remove_finding_mutate" },
      { action: "api_mutations_submit_draft_mutate" },
    ]);
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <FindingActions
          hasSubmission={false}
          hasVulns={false}
          isDraft={true}
          loading={false}
          onApprove={jest.fn()}
          onDelete={jest.fn()}
          onReject={jest.fn()}
          onSubmit={jest.fn()}
        />
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryAllByRole("button")).toHaveLength(2);
    expect(screen.queryByText("group.drafts.submit.text")).toBeInTheDocument();
    expect(
      screen.queryByText("searchFindings.delete.btn.text")
    ).toBeInTheDocument();
  });

  it("should render approver draft actions", (): void => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_approve_draft_mutate" },
      { action: "api_mutations_reject_draft_mutate" },
      { action: "api_mutations_remove_finding_mutate" },
      { action: "api_mutations_submit_draft_mutate" },
    ]);
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <FindingActions
          hasSubmission={false}
          hasVulns={true}
          isDraft={true}
          loading={false}
          onApprove={jest.fn()}
          onDelete={jest.fn()}
          onReject={jest.fn()}
          onSubmit={jest.fn()}
        />
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryAllByRole("button")).toHaveLength(4);
    expect(screen.queryByText("group.drafts.approve.text")).toBeInTheDocument();
    expect(screen.queryByText("group.drafts.submit.text")).toBeInTheDocument();
    expect(screen.queryByText("group.drafts.reject.text")).toBeInTheDocument();
    expect(
      screen.queryByText("searchFindings.delete.btn.text")
    ).toBeInTheDocument();
  });

  it("should disable approve button", (): void => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_approve_draft_mutate" },
    ]);
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <FindingActions
          hasSubmission={false}
          hasVulns={false}
          isDraft={true}
          loading={false}
          onApprove={jest.fn()}
          onDelete={jest.fn()}
          onReject={jest.fn()}
          onSubmit={jest.fn()}
        />
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryAllByRole("button")).toHaveLength(1);
    expect(screen.queryByText("group.drafts.approve.text")).toBeInTheDocument();
    expect(screen.queryByText("group.drafts.approve.text")).toBeDisabled();
  });
});
