import { useState, useImperativeHandle } from "react";

export default function FileUpload({ref}: any) {

    const [files, setFiles] = useState<File[]>([]);
    const [filesIsValid, setFilesIsValid] = useState(true)

    const colorInputField = filesIsValid ? "border-gray-300" : "border-red-300"

    useImperativeHandle(ref, ()=>{
        return {
            getFiles() {
                return files;
            },
            
            setFilesIsValid(value: boolean){
                setFilesIsValid(value)
            },

            checkFilesIsValid() {
                return filesIsValid;
            }
        }
    }, [files, filesIsValid])

    function handleFileChange(
        event: React.ChangeEvent<HTMLInputElement>
    ) {
        const selectedFiles = event.target.files;

        if (!selectedFiles) return;

        setFiles(Array.from(selectedFiles));
    }

    return (
        <div>
            <label
                htmlFor="file-upload"
                className={`
                    flex cursor-pointer flex-col items-center justify-center
                    rounded-2xl border-2 border-dashed ${colorInputField} bg-gray-50 px-6 py-10 text-center
                `}
            >
                <p className="font-medium">
                    Clique para adicionar arquivos
                </p>

                <p className="text-sm text-gray-500">
                    PDF
                </p>

                <input
                    id="file-upload"
                    ref={ref}
                    type="file"
                    multiple
                    accept=".pdf,.docx,.txt"
                    onChange={handleFileChange}
                    className="hidden"
                    required
                />
            </label>

            <div className="mt-4 flex flex-col gap-2">
                {files.map((file, index) => (
                    <div
                        key={`${file.name}-${index}`}
                        className="rounded-xl border px-4 py-3"
                    >
                        <p>{file.name}</p>

                        <p className="text-sm text-gray-500">
                            {(file.size / 1024 / 1024).toFixed(2)} MB
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
}