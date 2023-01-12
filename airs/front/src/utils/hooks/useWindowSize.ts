import { useEffect, useState } from "react";

interface IWindowSize {
  height: number;
  width: number;
}

const getSize = (): IWindowSize => {
  const { innerHeight, innerWidth } = window;

  return { height: innerHeight, width: innerWidth };
};

// Get window size reacting to changes
const useWindowSize = (): IWindowSize => {
  const [size, setSize] = useState(getSize());

  useEffect((): (() => void) => {
    const handleResize = (): void => {
      setSize(getSize());
    };
    window.addEventListener("resize", handleResize);

    return (): void => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  return size;
};

export { useWindowSize };
