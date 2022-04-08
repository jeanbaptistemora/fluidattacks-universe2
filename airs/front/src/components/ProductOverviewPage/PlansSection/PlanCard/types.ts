interface IPlansCard {
  isMachine: boolean;
  items: {
    check: boolean;
    text: string;
  }[];
  description: string;
  title: string;
}

export { IPlansCard };
