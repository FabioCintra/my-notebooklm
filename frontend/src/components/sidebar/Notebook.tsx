import type { NotebookProps } from "../types/NotebookProps.ts";

export default function Notebook({name, id}: NotebookProps) {

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
        >
            {name}
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