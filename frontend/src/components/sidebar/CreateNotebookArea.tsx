import { useRef, useState } from "react";
import FileUpload from "./FileUpload";
import type { FilesInputHandle } from "../types/FilesInputHandle";
import type { FileEncoded } from "../types/FileEncoded";
import { fileToBase64 } from "../../utils";
import type { CreateNotebookAreaProps } from "../types/props/CreateNotebookAreaProps";
import type { CreateNotebookRequest } from "../types/CreateNotebookRequest";
import type { NotebookProps } from "../types/props/NotebookProps";

export default function CreateNotebookArea({addNotebook, onClose}: CreateNotebookAreaProps){

    const nameNotebook = useRef<HTMLInputElement>(null)
    const files = useRef<FilesInputHandle>(null)

    const [nameNotebookIsValid, setNameNotebookIsValid] = useState(true)

    async function handleSubmit(event: any) {

        event.preventDefault();

        let requestIsValid: boolean = true;
        
        const name: string =  (nameNotebook.current) ? nameNotebook.current.value : "";
        const filesList: File[] = (files.current?.getFiles()) ? Array.from(files.current.getFiles()) : [];

        //Checando se todos os dados passados estao validos
        if (name === ""){
            requestIsValid = false;
            setNameNotebookIsValid(false);
        }

        if (filesList.length === 0){
            requestIsValid = false;
            files.current?.setFilesIsValid(false);
        }

        // Cancela a operacao caso os dados nao estajam validos
        if (!requestIsValid) {
            return;
        }
        else{
            files.current?.setFilesIsValid(true);
            setNameNotebookIsValid(true);
        }

        // Gerando a base64 dos arquivos
        const filesRequestList: FileEncoded[] = await Promise.all(
            filesList.map(async (file) => {
                const base64 = await fileToBase64(file);

                return {
                    file_name: file.name,
                    mime_type: file.type,
                    base64: base64
                }
            })
        )

        // Fazendo a requesicao
        const body: CreateNotebookRequest = {
            name_notebook: name,
            documents: filesRequestList
        }

        const result = await fetch("http://127.0.0.1:8000/notebooks/",
            {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-type": "application/json"
                },
                body: JSON.stringify(body)
            }
        )

        // Obtendo o resultado da requesicao
        const newNotebook: NotebookProps = await result.json()

        // Salvando
        addNotebook(newNotebook)
        onClose()

    }

    return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
        <div
            className="
                relative
                w-full
                max-w-lg
                rounded-2xl
                bg-white
                p-8
                shadow-xl
            "
        >
            {/* Botão fechar */}
            <button
                type="button"
                className="
                    absolute
                    right-4
                    top-4
                    flex
                    h-8
                    w-8
                    items-center
                    justify-center
                    rounded-full
                    text-lg
                    text-gray-500
                    transition
                    hover:bg-gray-100
                    hover:text-gray-900
                "
                onClick={onClose}
            >
                ×
            </button>

            {/* Título */}
            <div className="mb-7 text-center">
                <h2 className="text-2xl font-semibold text-gray-900">
                    Criar notebook
                </h2>

                <p className="mt-1 text-sm text-gray-500">
                    Escolha um nome e adicione os arquivos que farão parte dele.
                </p>
            </div>

            <form
                onSubmit={handleSubmit}
                className="flex flex-col gap-6"
            >
                {/* Nome */}
                <div className="flex flex-col gap-2">
                    <label
                        htmlFor="name_notebook"
                        className="text-sm font-medium text-gray-700"
                    >
                        Nome do Notebook
                    </label>

                    <input
                        type="text"
                        ref={nameNotebook}
                        id="name_notebook"
                        required
                        onChange={() => {
                            if (!nameNotebookIsValid) {
                                setNameNotebookIsValid(true);
                            }
                        }}
                        placeholder="Ex: Inteligência Artificial"
                        className={`
                            w-full
                            rounded-xl
                            border
                            px-4
                            py-3
                            text-sm
                            outline-none
                            transition
                            placeholder:text-gray-400

                            ${
                                nameNotebookIsValid
                                    ? `
                                        border-gray-300
                                        focus:border-gray-500
                                        focus:ring-2
                                        focus:ring-gray-100
                                    `
                                    : `
                                        border-red-500
                                        bg-red-50
                                        focus:border-red-500
                                        focus:ring-2
                                        focus:ring-red-100
                                    `
                            }
                        `}
                    />

                    {!nameNotebookIsValid && (
                        <p className="text-sm text-red-500">
                            Esse nome não pode ser utilizado.
                        </p>
                    )}
                </div>

                {/* Arquivos */}
                <FileUpload ref={files} />

                {/* Criar */}
                <button
                    type="submit"
                    className="
                        mt-2
                        w-full
                        rounded-xl
                        bg-gray-900
                        px-4
                        py-3
                        text-sm
                        font-medium
                        text-white
                        transition
                        hover:bg-gray-800
                        active:scale-[0.99]
                    "
                >
                    Criar notebook
                </button>
            </form>
        </div>
    </div>
);

}