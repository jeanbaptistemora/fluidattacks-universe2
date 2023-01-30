import { faFile } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import { ExternalLink } from "components/ExternalLink";

interface IDisplayImageProps {
  content: string;
  extension: string;
  name: string;
  onClick?: () => void;
}

const DisplayImage: React.FC<Readonly<IDisplayImageProps>> = ({
  content,
  extension,
  name,
  onClick,
}): JSX.Element => {
  const { t } = useTranslation();

  if (content === "") {
    return <div />;
  }

  if (content === "file") {
    return (
      // eslint-disable-next-line jsx-a11y/click-events-have-key-events
      <div onClick={onClick} role={"button"} tabIndex={0}>
        <FontAwesomeIcon icon={faFile} size={"1x"} />
      </div>
    );
  }

  if (extension === "webm") {
    return (
      <video controls={true} muted={true}>
        <source src={content} type={"video/webm"} />
        <p>
          {t("searchFindings.tabEvidence.altVideo.first")}&nbsp;
          <ExternalLink href={content}>
            {t("searchFindings.tabEvidence.altVideo.second")}
          </ExternalLink>
          &nbsp;{t("searchFindings.tabEvidence.altVideo.third")}
        </p>
      </video>
    );
  }

  return (
    // eslint-disable-next-line jsx-a11y/click-events-have-key-events
    <div onClick={onClick} role={"button"} tabIndex={0}>
      <img alt={name} src={content} />
    </div>
  );
};

export { DisplayImage };
