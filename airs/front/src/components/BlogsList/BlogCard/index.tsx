/* eslint require-unicode-regexp:0 */
/* eslint react/forbid-component-props:0 */
/* eslint @typescript-eslint/no-magic-numbers:0 */
import { Link } from "gatsby";
import { decode } from "he";
import { utc } from "moment";
import React from "react";

import {
  CardButtonContainer,
  CardDate,
  CardDescription,
  CardInnerDiv,
  CardSubTitle,
  CardTitle,
  MainBlogCard,
  PostInfo,
} from "../StyledComponents";

interface IProps {
  alt: string;
  blogLink: string;
  date: string;
  description: string;
  image: string;
  subtitle: string;
  title: string;
}

export const BlogCard: React.FC<IProps> = ({
  alt,
  blogLink,
  date,
  description,
  image,
  subtitle,
  title,
}: IProps): JSX.Element => {
  const fDate = utc(date.toLocaleString()).format("LL");

  return (
    <MainBlogCard>
      <img alt={alt} className={"br3 br--top"} src={image} />
      <CardInnerDiv>
        <CardDate>{fDate}</CardDate>
        <Link className={"no-underline"} to={`/blog/${blogLink}`}>
          <CardTitle>{decode(title)}</CardTitle>
        </Link>
        <CardSubTitle>{decode(subtitle)}</CardSubTitle>
        <PostInfo>
          <CardDescription>{description}</CardDescription>
          <CardButtonContainer>
            <Link
              className={
                "c-fluid-bk f5 mt6 hv-fluid-rd fw4 no-underline t-all-5"
              }
              to={`/blog/${blogLink}`}
            >
              <button className={"button-white w-80"}>{"Read post"}</button>
            </Link>
          </CardButtonContainer>
        </PostInfo>
      </CardInnerDiv>
    </MainBlogCard>
  );
};
