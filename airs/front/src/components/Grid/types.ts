type Nums1To4 = 1 | 2 | 3 | 4;

interface IGridProps {
  children: React.ReactNode;
  columns: Nums1To4;
  columnsMd?: Nums1To4;
  columnsSm?: Nums1To4;
  gap: string;
  pv?: string;
  ph?: string;
}

export type { IGridProps, Nums1To4 };
