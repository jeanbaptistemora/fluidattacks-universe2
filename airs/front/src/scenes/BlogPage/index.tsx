import React from "react";

import { ContentSection } from "./ContentSection";
import { CtaSection } from "./CtaSection";
import { HeaderSection } from "./HeaderSection";
import { InfoSection } from "./InfoSection";
import { SlideSection } from "./SlideSection";
import { SubscribeSection } from "./SubscribeSection";
import { TagsSection } from "./TagsSection";

interface ISolutionPageProps {
  author: string;
  category: string;
  date: string;
  description: string;
  htmlAst: string;
  image: string;
  slug: string;
  subtitle: string;
  tags: string;
  title: string;
  writer: string;
}

const BlogPage: React.FC<ISolutionPageProps> = ({
  author,
  category,
  description,
  date,
  htmlAst,
  image,
  slug,
  subtitle,
  tags,
  title,
  writer,
}): JSX.Element => {
  return (
    <React.Fragment>
      <HeaderSection
        category={category}
        description={description}
        image={image}
        subtitle={subtitle}
        title={title}
      />
      <InfoSection author={author} date={date} writer={writer} />
      <ContentSection htmlAst={htmlAst} slug={slug} />
      <TagsSection tags={tags} />
      <SubscribeSection />
      <SlideSection slug={slug} tags={tags} />
      <CtaSection />
    </React.Fragment>
  );
};

export { BlogPage };
