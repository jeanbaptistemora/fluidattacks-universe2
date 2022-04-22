import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { Comments } from "scenes/Dashboard/components/Comments";
import { CommentEditor } from "scenes/Dashboard/components/Comments/components/CommentEditor";
import { NestedComment } from "scenes/Dashboard/components/Comments/components/NestedComment";
import { commentContext } from "scenes/Dashboard/components/Comments/context";
import type { ICommentStructure } from "scenes/Dashboard/components/Comments/types";

describe("Comments section", (): void => {
  const onLoadComments: jest.Mock = jest.fn();
  const onPostComment: jest.Mock = jest.fn();

  const mockComment: ICommentStructure = {
    content: "Hello world",
    created: "2021/04/20 00:00:01",
    createdByCurrentUser: true,
    email: "unittest@fluidattacks.com",
    fullName: "Test User",
    id: 1337260012345,
    modified: "2021/04/20 00:00:01",
    parentComment: 0,
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Comments).toBe("function");
  });

  it("should render an empty comment section", (): void => {
    expect.hasAssertions();

    render(<Comments onLoad={jest.fn()} onPostComment={jest.fn()} />);

    expect(screen.getByRole("textbox")).toBeInTheDocument();

    userEvent.clear(screen.getByRole("textbox"));
    userEvent.type(screen.getByRole("textbox"), "test comment");

    expect(screen.getAllByRole("button")).toHaveLength(1);
    expect(screen.queryByText("comments.noComments")).toBeInTheDocument();
  });

  it("should load comments on render", async (): Promise<void> => {
    expect.hasAssertions();

    render(<Comments onLoad={onLoadComments} onPostComment={jest.fn()} />);

    await waitFor((): void => {
      expect(onLoadComments).toHaveBeenCalledTimes(1);
    });
    jest.clearAllMocks();
  });

  it("should post a comment", async (): Promise<void> => {
    expect.hasAssertions();

    render(<CommentEditor id={0} onPost={onPostComment} />);

    expect(screen.getByRole("textbox")).toBeInTheDocument();
    expect(screen.queryByText("comments.send")).not.toBeInTheDocument();

    userEvent.clear(screen.getByRole("textbox"));
    userEvent.type(screen.getByRole("textbox"), "test comment");
    await waitFor((): void => {
      expect(screen.queryByText("comments.send")).toBeInTheDocument();
    });
    userEvent.click(screen.getByText("comments.send"));
    await waitFor((): void => {
      expect(onPostComment).toHaveBeenCalledTimes(1);
    });
  });

  it("should render a single comment", async (): Promise<void> => {
    expect.hasAssertions();

    const { container } = render(
      <commentContext.Provider value={{ replying: mockComment.id }}>
        <NestedComment
          backgroundEnabled={false}
          comments={[mockComment]}
          id={mockComment.id}
          onPost={jest.fn()}
          orderBy={"newest"}
        />
      </commentContext.Provider>
    );

    expect(container.querySelectorAll(".comment-nested")).toHaveLength(1);
    expect(
      container.querySelectorAll(".comment-content")[0].textContent
    ).toContain(mockComment.content);
    expect(
      container.querySelectorAll(".comment-datetime")[0].textContent
    ).toContain(mockComment.created);

    userEvent.click(screen.getByText("comments.reply"));
    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "comment-editor" })
      ).toBeInTheDocument();
    });
  });
});
