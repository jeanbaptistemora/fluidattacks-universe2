/* eslint require-unicode-regexp:0 */
/* eslint react/forbid-component-props:0 */
/* eslint @typescript-eslint/no-magic-numbers:0 */
import { Link } from "gatsby";
import { decode } from "he";
import React from "react";

import { stringToUri } from "../../../utils/utilities";
import {
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
  const taglist: string[] = tags.split(", ");

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
          <CardText>
            {"Author:"}&nbsp;
            <Link
              className={"c-fluid-gray hv-fluid-black no-underline"}
              to={`/blog/authors/${stringToUri(author)}`}
            >
              {author}
            </Link>
          </CardText>
          <CardText>
            {"Category:"}&nbsp;
            {
              <Link
                className={"c-fluid-gray hv-fluid-black no-underline"}
                to={`/blog/categories/${category.toLowerCase()}`}
              >
                {category.replace("-", " ")}
              </Link>
            }
          </CardText>
          <CardText>
            {"Tags:"}&nbsp;
            {taglist.map(
              (tag: string, index): JSX.Element =>
                taglist.length === index + 1 ? (
                  <Link
                    className={"c-fluid-gray hv-fluid-black no-underline"}
                    to={`/blog/tags/${tag}`}
                  >{`${tag}`}</Link>
                ) : (
                  <Link
                    className={"c-fluid-gray hv-fluid-black no-underline"}
                    to={`/blog/tags/${tag}`}
                  >{`${tag}, `}</Link>
                )
            )}
          </CardText>
          <CardDescription>{`${description.slice(0, 100)}...`}</CardDescription>
          <br />
          <br />
          <CardButtonContainer>
            <Link
              className={
                "c-fluid-bk f5 mt6 hv-fluid-rd fw4 no-underline t-all-5"
              }
              to={`/blog/${blogLink}`}
            >
              <button className={"button-white w-80"}>{"Read Post"}</button>
            </Link>
          </CardButtonContainer>
        </PostInfo>
      </CardInnerDiv>
    </MainBlogCard>
  );
};
