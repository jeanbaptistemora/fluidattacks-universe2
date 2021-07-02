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
  alt: string;
  cardType: string;
  haveTitle: boolean;
  htmlData: string;
  logo: string;
  logoPaths: string;
  slug: string;
  title: string;
}

const DropDownCard: React.FC<IProps> = ({
  alt,
  cardType,
  haveTitle,
  htmlData,
  logo,
  logoPaths,
  slug,
  title,
}: IProps): JSX.Element => {
  const [isTouch, setIsTouch] = useState(false);
  const handleOpenClose = useCallback((): void => {
    setIsTouch(!isTouch);
  }, [isTouch]);

  return (
    <CardContainer className={cardType} key={slug}>
      <CardHeader onClick={handleOpenClose}>
        <CloudImage alt={alt} src={`${logoPaths}/${logo}`} />
        <br />
        {haveTitle ? (
          <React.Fragment>
            <br />
            <div className={"mb5"}>
              <h4>{title}</h4>
            </div>
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
          marginTop: isTouch ? "-3rem" : "0",
        }}
      >
        <div
          className={"down-cards"}
          dangerouslySetInnerHTML={{
            __html: htmlData,
          }}
        />
      </CardBody>
    </CardContainer>
  );
};
export { DropDownCard };
