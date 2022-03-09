export function commitFormatter(value: string): string {
  const COMMIT_LENGTH: number = 7;

  return value.slice(0, COMMIT_LENGTH);
}
