import { Link } from "gatsby";
import React from "react";

import { DropDownQuestion } from "./DropDownQuestion";
import { Container, FaqContainer, FaqParagraph } from "./styledComponents";

import { translate } from "../../../utils/translations/translate";

const FaqSection: React.FC = (): JSX.Element => {
  const data = [
    {
      answers: [
        { answer: translate.t("productOverview.faqSection.question1Answer") },
      ],
      hasLink: true,
      isList: false,
      title: translate.t("productOverview.faqSection.question1Title"),
    },
    {
      answers: [
        {
          answer: translate.t("productOverview.faqSection.question2Answer.a1"),
        },
        {
          answer: translate.t("productOverview.faqSection.question2Answer.a2"),
        },
        {
          answer: translate.t("productOverview.faqSection.question2Answer.a3"),
        },
        {
          answer: translate.t("productOverview.faqSection.question2Answer.a4"),
        },
        {
          answer: translate.t("productOverview.faqSection.question2Answer.a5"),
        },
        {
          answer: translate.t("productOverview.faqSection.question2Answer.a6"),
        },
      ],
      hasLink: false,
      isList: true,
      title: translate.t("productOverview.faqSection.question2Title"),
    },
    {
      answers: [
        {
          answer: translate.t("productOverview.faqSection.question3Answer.a1"),
        },
        {
          answer: translate.t("productOverview.faqSection.question3Answer.a2"),
        },
        {
          answer: translate.t("productOverview.faqSection.question3Answer.a3"),
        },
      ],
      hasLink: false,
      isList: true,
      title: translate.t("productOverview.faqSection.question3Title"),
    },
    {
      answers: [
        { answer: translate.t("productOverview.faqSection.question4Answer") },
      ],
      hasLink: false,
      isList: false,
      title: translate.t("productOverview.faqSection.question4Title"),
    },
  ];

  return (
    <Container>
      <FaqContainer>
        {data.map((question): JSX.Element => {
          return (
            <DropDownQuestion
              answers={question.answers}
              hasLink={question.hasLink}
              isList={question.isList}
              key={`question-${question.title}`}
              title={question.title}
            />
          );
        })}
        <FaqParagraph>
          {translate.t("productOverview.faqSection.paragraph")}
          <Link to={"/faq"}>{"here."}</Link>
        </FaqParagraph>
      </FaqContainer>
    </Container>
  );
};

export { FaqSection };
