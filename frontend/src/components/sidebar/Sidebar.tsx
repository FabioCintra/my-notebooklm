import { useEffect, useState } from "react";

import Notebook from "./Notebook";
import type { NotebookProps } from "../types/NotebookProps";

export default function Sidebar(){

    const [notebooks, setNotebooks] = useState<NotebookProps[]>([])

    function handleNotebooks(notebooks: NotebookProps[] | NotebookProps){
        setNotebooks(oldNotebooks => {
            if (Array.isArray(notebooks)){
                return notebooks
            }

            return [
                ...oldNotebooks,
                notebooks
            ]
        })
    }

    return (
        <div className="flex h-screen w-64 flex-col border-r border-gray-200 bg-white p-3">

            <div className="flex items-center justify-between">
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
                >
                    +
                </button>
            </div>

            <div className="mt-3 -mx-2 flex flex-col gap-1 overflow-y-auto">
                {notebooks.map(note => (
                    <Notebook
                        key={note.id}
                        name={note.name}
                        id={note.id}
                    />
                ))}
            </div>

        </div>
    );

}