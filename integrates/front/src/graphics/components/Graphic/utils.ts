export function hasIFrameError(
  iFrameRef: React.MutableRefObject<HTMLIFrameElement | null>
): boolean {
  return Boolean(
    iFrameRef.current?.contentDocument?.title.toLowerCase().includes("error")
  );
}
