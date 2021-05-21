/* eslint react/no-danger: 0 */
/* eslint react/forbid-component-props: 0 */
import { faChevronDown, faChevronUp } from "@fortawesome/pro-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback, useState } from "react";

import {
  CardBody,
  CardContainer,
  CardHeader,
  CardReadMore,
} from "../../styles/styledComponents";
import { CloudImage } from "../CloudImage";

interface IProps {
  haveTitle: boolean;
  node: {
    fields: {
      slug: string;
    };
    document: {
      title: string;
    };
    html: string;
    pageAttributes: {
      alt: string;
      description: string;
      keywords: string;
      partner: string;
      partnerlogo: string;
      slug: string;
    };
  };
}

const DropDownCard: React.FC<IProps> = ({
  node,
  haveTitle,
}: IProps): JSX.Element => {
  const { pageAttributes, html: htmlData, document } = node;
  const [isTouch, setIsTouch] = useState(false);
  const handleOpenClose = useCallback((): void => {
    setIsTouch(!isTouch);
  }, [isTouch]);

  return (
    <CardContainer key={pageAttributes.slug}>
      <CardHeader onClick={handleOpenClose}>
        <CloudImage
          alt={pageAttributes.alt}
          src={`/airs/partners/${pageAttributes.partnerlogo}`}
        />
        <br />
        {haveTitle ? (
          <React.Fragment>
            <br />
            <h4>{document.title}</h4>
          </React.Fragment>
        ) : undefined}
        <CardReadMore>
          {isTouch ? undefined : "Read More"}
          <br />
          <FontAwesomeIcon
            className={"arrow w1 pv3"}
            icon={isTouch ? faChevronUp : faChevronDown}
          />
        </CardReadMore>
      </CardHeader>
      <CardBody
        style={{
          height: isTouch ? "30rem" : "0",
        }}
      >
        <div
          dangerouslySetInnerHTML={{
            __html: htmlData,
          }}
        />
      </CardBody>
    </CardContainer>
  );
};
export { DropDownCard };
