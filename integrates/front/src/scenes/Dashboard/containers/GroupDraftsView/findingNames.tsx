interface IResponseStructure {
  feed: { entry: IRowStructure[] };
}
interface IRowStructure {
  gsx$cwe: { $t: string };
  gsx$descripcion: { $t: string };
  gsx$fin: { $t: string };
  gsx$recomendacion: { $t: string };
  gsx$requisito: { $t: string };
  gsx$tipo: { $t: string };
}
interface ISuggestion {
  cwe: string;
  description: string;
  recommendation: string;
  requirements: string;
  title: string;
  type: string;
}
async function getFindingNames(): Promise<ISuggestion[]> {
  const baseUrl: string = "https://spreadsheets.google.com/feeds/list";
  const spreadsheetId: string = "1L37WnF6enoC8Ws8vs9sr0G29qBLwbe-3ztbuopu1nvc";
  const rowOffset: number = 2;
  const extraParams: string = `&min-row=${rowOffset}`;
  const response: Response = await fetch(
    `${baseUrl}/${spreadsheetId}/1/public/values?alt=json${extraParams}`
  );
  const body: IResponseStructure | undefined = await response.json();

  if (body?.feed.entry) {
    return body.feed.entry.map((row: IRowStructure): ISuggestion => {
      const cwe: RegExpMatchArray | null = row.gsx$cwe.$t.match(/\d+/gu);

      return {
        cwe: cwe === null ? "" : cwe[0],
        description: row.gsx$descripcion.$t,
        recommendation: row.gsx$recomendacion.$t,
        requirements: row.gsx$requisito.$t,
        title: row.gsx$fin.$t,
        type: row.gsx$tipo.$t === "Seguridad" ? "SECURITY" : "HYGIENE",
      };
    });
  }

  return [];
}

export { IResponseStructure, IRowStructure, ISuggestion, getFindingNames };
