/* eslint react/forbid-component-props:0 */
/* eslint @typescript-eslint/no-magic-numbers:0 */
import { Link } from "gatsby";
import { decode } from "he";
import React from "react";

import {
  CardButton,
  CardButtonContainer,
  CardDescription,
  CardInnerDiv,
  CardSubTitle,
  CardText,
  CardTitle,
  MainBlogCard,
  PostInfo,
} from "../StyledComponents";

interface IProps {
  alt: string;
  author: string;
  blogLink: string;
  category: string;
  description: string;
  image: string;
  subtitle: string;
  tags: string;
  title: string;
}

export const BlogCard: React.FC<IProps> = ({
  alt,
  author,
  blogLink,
  category,
  description,
  image,
  subtitle,
  tags,
  title,
}: IProps): JSX.Element => {
  return (
    <MainBlogCard>
      <img alt={alt} className={"br3 br--top"} src={image} />
      <CardInnerDiv>
        <Link className={"no-underline"} to={`/blog/${blogLink}`}>
          <CardTitle>{decode(title)}</CardTitle>
        </Link>
        <CardSubTitle>{decode(subtitle)}</CardSubTitle>
        <br />
        <PostInfo>
          <CardText>{`Author: ${author}`}</CardText>
          <CardText>{`Category: ${category.replace("-", " ")}`}</CardText>
          <CardText>{`Tags: ${tags}`}</CardText>
          <CardDescription>{`${description.slice(0, 100)}...`}</CardDescription>
          <br />
          <br />
          <CardButtonContainer>
            <Link className={"no-underline"} to={blogLink}>
              <CardButton>{"Read More"}</CardButton>
            </Link>
          </CardButtonContainer>
        </PostInfo>
      </CardInnerDiv>
    </MainBlogCard>
  );
};
