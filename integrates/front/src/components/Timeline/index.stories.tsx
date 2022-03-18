/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import { Timeline, TimelineItem } from ".";

const config: Meta = {
  component: Timeline,
  subcomponents: { TimelineItem },
  title: "components/Timeline",
};

const Default: Story = (): JSX.Element => {
  return (
    <Timeline>
      <TimelineItem>
        <h2>{"2020-06-17"}</h2>
        <h3>{"Lorem ipsum"}</h3>
        <p>{"Lorem ipsum dolor sit amet, consectetur adipiscing elit."}</p>
      </TimelineItem>
      <TimelineItem>
        <h2>{"2020-06-18"}</h2>
        <h3>{"Lorem ipsum"}</h3>
        <p>{"Lorem ipsum dolor sit amet, consectetur adipiscing elit."}</p>
      </TimelineItem>
      <TimelineItem>
        <h2>{"2020-06-19"}</h2>
        <h3>{"Lorem ipsum"}</h3>
        <p>{"Lorem ipsum dolor sit amet, consectetur adipiscing elit."}</p>
      </TimelineItem>
      <TimelineItem>
        <h2>{"2020-06-20"}</h2>
        <h3>{"Lorem ipsum"}</h3>
        <p>{"Lorem ipsum dolor sit amet, consectetur adipiscing elit."}</p>
      </TimelineItem>
    </Timeline>
  );
};

export { Default };
export default config;
