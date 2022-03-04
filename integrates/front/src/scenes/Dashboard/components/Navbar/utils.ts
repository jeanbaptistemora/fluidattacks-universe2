const clickedPortal = (event: Event): boolean => {
  const path = event.composedPath();
  const appRootIndex = 5;

  return (path[path.length - appRootIndex] as HTMLElement).id !== "root";
};

export { clickedPortal };
