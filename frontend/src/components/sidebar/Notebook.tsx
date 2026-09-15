import type { NotebookProps } from "../types/NotebookProps.ts";
import { useContext } from "react";
import { ChatContext } from "../../store/ChatContext.tsx";

export default function Notebook({name_notebook, thread_id}: NotebookProps) {

    const chatCtx = useContext(ChatContext)

    return (
    <div className="flex w-full items-center justify-between px-3 py-2 rounded-2xl hover:bg-gray-200">
        <button
            className="
                flex-1
                truncate
                text-left
                text-sm
                font-semibold
                text-gray-900
            "
            onClick={() => chatCtx.setId(thread_id)}
        >
            {name_notebook}
        </button>

        <button
            className="
                ml-2
                flex
                h-7
                w-7
                shrink-0
                items-center
                justify-center
                rounded-md
                text-lg
                font-semibold
                text-gray-700
                transition-colors
                hover:bg-gray-200
            "
        >
            ...
        </button>
    </div>
);

}