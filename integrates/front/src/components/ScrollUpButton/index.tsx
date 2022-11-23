import { faArrowUp } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FC } from "react";
import React, { useCallback, useEffect, useState } from "react";
import styled from "styled-components";

import { Button } from "components/Button";

const FloatButton = styled.div.attrs({
  className: "comp-scroll-up",
})`
  bottom: 15px;
  position: fixed;
  right: 140px;
  z-index: 100;
`;

interface IScrollUpButtonProps {
  scrollerId?: string;
  visibleAt?: number;
}

const ScrollUpButton: FC<IScrollUpButtonProps> = ({
  scrollerId = "dashboard",
  visibleAt = 500,
}: Readonly<IScrollUpButtonProps>): JSX.Element | null => {
  const [visible, setVisible] = useState(false);
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

  return visible ? (
    <FloatButton>
      <Button id={"scroll-up"} onClick={goToTop} variant={"primary"}>
        <FontAwesomeIcon icon={faArrowUp} />
      </Button>
    </FloatButton>
  ) : null;
};

export { ScrollUpButton };
