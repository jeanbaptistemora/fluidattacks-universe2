import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import TextArea from "react-textarea-autosize";
import wait from "waait";

import { Button } from "components/Button";
import { Comments, commentContext } from "scenes/Dashboard/components/Comments";
import { CommentEditor } from "scenes/Dashboard/components/Comments/components/CommentEditor";
import { NestedComment } from "scenes/Dashboard/components/Comments/components/NestedComment";
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
    parent: 0,
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Comments).toStrictEqual("function");
  });

  it("should render an empty comment section", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Comments onLoad={jest.fn()} onPostComment={jest.fn()} />
    );

    const editorTextArea: ReactWrapper = wrapper
      .find(CommentEditor)
      .find(TextArea);

    editorTextArea.simulate("change", { target: { value: "test comment" } });

    const editorButton: ReactWrapper = wrapper.find(CommentEditor).find(Button);

    expect(wrapper).toHaveLength(1);
    expect(editorTextArea).toHaveLength(1);
    expect(editorButton).toHaveLength(1);
    expect(wrapper.find("#no-comments")).toHaveLength(1);
  });

  it("should load comments on render", async (): Promise<void> => {
    expect.hasAssertions();

    mount(<Comments onLoad={onLoadComments} onPostComment={jest.fn()} />);

    await wait(0);

    expect(onLoadComments).toHaveBeenCalledTimes(1);
  });

  it("should post a comment", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <CommentEditor id={0} onPost={onPostComment} />
    );

    wrapper
      .find(TextArea)
      .simulate("change", { target: { value: "test comment" } });

    const editorButton: ReactWrapper = wrapper.find(Button);

    editorButton.simulate("click");

    expect(onPostComment).toHaveBeenCalledTimes(1);
  });

  it("should render a single comment", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
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

    expect(wrapper.find(".comment-nested")).toHaveLength(1);
    expect(wrapper.find(".comment-content").text()).toContain(
      mockComment.content
    );
    expect(wrapper.find(".comment-datetime").text()).toContain(
      mockComment.created
    );

    const replyButton: ReactWrapper = wrapper.find(".comment-reply");
    replyButton.simulate("click");

    expect(wrapper.find(CommentEditor)).toHaveLength(1);
  });
});
