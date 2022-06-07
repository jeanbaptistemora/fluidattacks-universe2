import { faArrowUp } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import styled from "styled-components";

import { Button } from "components/Button";

const FloatButton = styled.div.attrs({
  className: "fixed",
  id: "scroll-up",
})`
  bottom: 8px;
  right: 16px;
  z-index: 100;
`;

interface IScrollUpButtonProps {
  scrollerId?: string;
  visibleAt?: number;
}

export const ScrollUpButton: React.FC<IScrollUpButtonProps> = ({
  scrollerId = "dashboard",
  visibleAt = 500,
}: Readonly<IScrollUpButtonProps>): JSX.Element => {
  const [visible, setVisible] = useState(false);
  const { t } = useTranslation();
  const [scroller, setScroller] = useState<HTMLElement | null>();

  useEffect((): void => {
    setScroller(document.getElementById(scrollerId));
    scroller?.addEventListener("scroll", (): void => {
      setVisible(scroller.scrollTop > visibleAt);
    });
  }, [scroller, scrollerId, visibleAt]);

  const goToTop = useCallback((): void => {
    scroller?.scrollTo({
      behavior: "smooth",
      top: 0,
    });
  }, [scroller]);

  return (
    <FloatButton>
      {visible && (
        <Button onClick={goToTop} variant={"primary"}>
          {t("components.scrollUpButton")}
          &nbsp;
          <FontAwesomeIcon icon={faArrowUp} />
        </Button>
      )}
    </FloatButton>
  );
};
