import type { FileEncoded } from "./FileEncoded";

export interface CreateNotebookRequest {
    name_notebook: string,
    documents: FileEncoded[]
}