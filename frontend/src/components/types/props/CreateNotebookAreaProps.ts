import type { NotebookProps } from "./NotebookProps"

export type CreateNotebookAreaProps = {
    addNotebook: (notebook: NotebookProps) => void,
    onClose: () => void
}