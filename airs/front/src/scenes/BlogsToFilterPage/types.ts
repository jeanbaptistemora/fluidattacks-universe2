interface IBlogsToFilterPageProps {
  description?: string;
  filterBy: "author" | "category" | "tag";
  title?: string;
  value: string;
}

export type { IBlogsToFilterPageProps };
