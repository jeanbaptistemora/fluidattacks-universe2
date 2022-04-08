/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React, { useCallback, useState } from "react";

import {
  AnswerContainer,
  AnswerItem,
  AnswerLabel,
  QuestionContainer,
  QuestionTitle,
} from "./styledComponents";

import { RotatingArrow } from "../../../RotatingArrow";

interface IDropDownQuestion {
  answers: {
    answer: string;
  }[];
  hasLink: boolean;
  isList: boolean;
  title: string;
}

const DropDownQuestion: React.FC<IDropDownQuestion> = ({
  answers,
  hasLink,
  isList,
  title,
}: IDropDownQuestion): JSX.Element => {
  const [isTouch, setIsTouch] = useState(false);
  const handleOpenClose = useCallback((): void => {
    setIsTouch(!isTouch);
  }, [isTouch]);

  return (
    <QuestionContainer>
      <QuestionTitle onClick={handleOpenClose}>
        <div className={"w-80"}>{title}</div>
        <div className={"w-20"}>
          <RotatingArrow isTouch={isTouch} />
        </div>
      </QuestionTitle>
      {isList ? (
        <AnswerContainer
          isItem={true}
          style={{
            animation: "fadein 0.5s",
            display: isTouch ? "block" : "none",
          }}
        >
          {answers.map((answer): JSX.Element => {
            return (
              <AnswerItem key={`${answer.answer}`}>{answer.answer}</AnswerItem>
            );
          })}
        </AnswerContainer>
      ) : (
        <AnswerContainer
          isItem={false}
          style={{
            animation: "fadein 0.5s",
            display: isTouch ? "block" : "none",
          }}
        >
          {answers.map((answer): JSX.Element => {
            return (
              <AnswerLabel key={`${answer.answer}`}>
                {answer.answer}
                {hasLink ? (
                  <Link to={"/about-us/clients/"}>{"here."}</Link>
                ) : undefined}
              </AnswerLabel>
            );
          })}
        </AnswerContainer>
      )}
    </QuestionContainer>
  );
};

export { DropDownQuestion };
