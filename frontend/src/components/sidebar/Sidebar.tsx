import { useEffect, useState} from "react";

import Notebook from "./Notebook";
import type { NotebookProps } from "../types/props/NotebookProps";
import CreateNotebookArea from "./CreateNotebookArea";

export default function Sidebar(){

    const [notebooks, setNotebooks] = useState<NotebookProps[]>([])
    const [showCreateNotebook, setShowCreateNotebook] = useState(false)

    useEffect(() => {
        async function fecthAllNootebooks(){

            const response = await fetch("http://127.0.0.1:8000/notebooks/",
                {
                    method: "GET",
                    credentials: "include"
                }
            )
            const notebooks: NotebookProps[] = await response.json()
     
            setNotebooks(notebooks)
        }

        fecthAllNootebooks()

    }, [])

    function addNotebook(notebook: NotebookProps){
        setNotebooks(oldNotebooks => {
            return [
                ...oldNotebooks,
                notebook
            ]
        })
    }

    return (
        <div className="flex h-screen w-64 flex-col border-r border-gray-200 bg-white p-3">

            <div className="flex items-center justify-between">

                {showCreateNotebook && (
                    <CreateNotebookArea
                        addNotebook={addNotebook}
                        onClose={() => setShowCreateNotebook(false)}
                    />
                )}

                 <h4 className="text-lg font-semibold tracking-tight text-gray-900">
                    Notebooks
                </h4>

                <button
                    className="
                        flex h-8 w-8 items-center justify-center
                        rounded-md
                        text-xl
                        font-medium
                        text-gray-700
                        transition-colors
                        hover:bg-gray-200
                    "
                    onClick={() => setShowCreateNotebook(true)}
                >
                    +
                </button>
            </div>

            <div className="mt-3 -mx-2 flex flex-col gap-1 overflow-y-auto">
                {notebooks.map(note => (
                    <Notebook
                        key={note.thread_id}
                        name_notebook={note.name_notebook}
                        thread_id={note.thread_id}
                    />
                ))}
            </div>

        </div>
    );

}