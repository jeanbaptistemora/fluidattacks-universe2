/* eslint @typescript-eslint/no-confusing-void-expression:0 */
import { useEffect } from "react";
import type { RefObject } from "react";

const events = [`mousedown`, `touchstart`];

export const useClickOutside = (
  ref: RefObject<HTMLDivElement>,
  onClickOutside: () => void
): void => {
  const isOutside = (element: HTMLElement): boolean =>
    !ref.current || !ref.current.contains(element);

  const onClick = (event: Event): void => {
    if (isOutside(event.target as HTMLElement)) {
      onClickOutside();
    }
  };

  useEffect((): (() => void) => {
    events.forEach((event): void => document.addEventListener(event, onClick));

    return (): void => {
      events.forEach((event): void =>
        document.removeEventListener(event, onClick)
      );
    };
  });
};
