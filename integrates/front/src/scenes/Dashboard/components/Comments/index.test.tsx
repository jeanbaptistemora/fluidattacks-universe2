import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { Comment } from "./Comment";
import { CommentEditor } from "./components/CommentEditor";
import { commentContext } from "./context";
import type { ICommentStructure } from "./types";

import { Comments } from ".";
import { authzGroupContext } from "utils/authz/config";

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

  it("should render an empty comment section", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <Comments
        isObservation={true}
        onLoad={jest.fn()}
        onPostComment={jest.fn()}
      />
    );

    expect(screen.getByRole("textbox")).toBeInTheDocument();

    await userEvent.clear(screen.getByRole("textbox"));
    await userEvent.type(screen.getByRole("textbox"), "test comment");

    expect(screen.getAllByRole("button")).toHaveLength(1);
    expect(screen.queryByText("comments.noComments")).toBeInTheDocument();
  });

  it("should load comments on render", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <Comments
        isObservation={true}
        onLoad={onLoadComments}
        onPostComment={jest.fn()}
      />
    );

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

    await userEvent.clear(screen.getByRole("textbox"));
    await userEvent.type(screen.getByRole("textbox"), "test comment");
    await waitFor((): void => {
      expect(screen.queryByText("comments.send")).toBeInTheDocument();
    });
    await userEvent.click(screen.getByText("comments.send"));
    await waitFor((): void => {
      expect(onPostComment).toHaveBeenCalledTimes(1);
    });
  });

  it("should render a single comment", async (): Promise<void> => {
    expect.hasAssertions();

    const { container } = render(
      <authzGroupContext.Provider
        value={new PureAbility([{ action: "has_squad" }])}
      >
        <commentContext.Provider value={{ replying: mockComment.id }}>
          <Comment
            backgroundEnabled={false}
            comments={[mockComment]}
            id={mockComment.id}
            isObservation={false}
            onPost={jest.fn()}
            orderBy={"newest"}
          />
        </commentContext.Provider>
      </authzGroupContext.Provider>
    );

    expect(container.querySelectorAll(".comment")).toHaveLength(1);

    await userEvent.click(screen.getByText("comments.reply"));
    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "comment-editor" })
      ).toBeInTheDocument();
    });
  });
});
