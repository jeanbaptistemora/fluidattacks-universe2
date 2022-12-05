/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { IVerticalCard } from "./types";

import { VerticalCard } from ".";

const config: Meta = {
  component: VerticalCard,
  title: "components/VerticalCard",
};

const TextTemplate: Story<IVerticalCard> = (props): JSX.Element => (
  <VerticalCard {...props} />
);

const Default = TextTemplate.bind({});
Default.args = {
  alt: "Photo by Sebastian Pena Lambarri on Unsplash",
  author: "Felipe Ruiz",
  btnText: "Read post",
  date: "2020-05-14",
  description:
    "Learn about what DevSecOps is, its importance, " +
    "how it differs from DevOps, and its advantages on IT security " +
    "for continuous delivery, testing and deployment.",
  image:
    "https://res.cloudinary.com/fluid-attacks/image/upload/v1620330852/blog/devsecops-concept/cover_c4reuk.webp",
  imagePadding: false,
  link: "",
  subtitle: "Best practices and a description of the basics",
  title: "What Is DevSecOps?",
  width: "450px",
};

const Simple: Story = (): JSX.Element => (
  <VerticalCard
    alt={"Photo by Sebastian Pena Lambarri on Unsplash"}
    btnText={"Read post"}
    description={
      "Learn about what DevSecOps is, its importance, " +
      "how it differs from DevOps, and its advantages on IT security " +
      "for continuous delivery, testing and deployment."
    }
    image={
      "https://res.cloudinary.com/fluid-attacks/image/upload/v1620330852/blog/devsecops-concept/cover_c4reuk.webp"
    }
    link={""}
    title={"What Is DevSecOps?"}
    width={"450px"}
  />
);

export { Default, Simple };
export default config;
