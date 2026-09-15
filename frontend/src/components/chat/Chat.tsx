import { useEffect, useContext, useState } from "react";
import { ChatContext } from "../../store/ChatContext";
import Messages from "./Messages";
import InputPrompt from "./InputPrompt";

export default function Chat(){

    const {messages,addMessage,id,setId} = useContext(ChatContext)
    const [notebookSelected, setnotebookSelected] = useState(false)

    useEffect(() => {

        function showMessages(){

            console.log(id)

            if (id != ""){
                setnotebookSelected(true)
            }

        }

        showMessages()

    },[messages])

    return (
    <div className="relative flex h-full w-full flex-col bg-white">
        {!notebookSelected ? (
            <div className="flex h-full flex-col items-center justify-center px-6 text-center">
                <div
                    className="
                        mb-4
                        flex h-14 w-14
                        items-center justify-center
                        rounded-2xl
                        bg-gray-100
                        text-gray-500
                    "
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="1.8"
                        className="h-7 w-7"
                    >
                        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
                        <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2Z" />
                    </svg>
                </div>

                <h2 className="text-lg font-semibold text-gray-800">
                    Nenhum notebook selecionado
                </h2>

                <p className="mt-1 max-w-sm text-sm text-gray-500">
                    Selecione um notebook na barra lateral para visualizar
                    suas mensagens e começar uma conversa.
                </p>
            </div>
        ) : (
            <>
                {/* Área das mensagens */}
                <div
                    className="
                        flex-1
                        overflow-y-auto
                        px-6
                        pb-32
                        pt-6
                    "
                >
                    <div className="mx-auto flex max-w-3xl flex-col gap-4">
                        {messages.map((message, index) => (
                            <Messages
                                key={index}
                                identifier={message.identifier}
                                message={message.message}
                            />
                        ))}
                    </div>
                </div>

                {/* Input sobreposto na parte inferior */}
                <div
                    className="
                        absolute
                        bottom-0
                        left-0
                        right-0
                        bg-gradient-to-t
                        from-white
                        via-white
                        to-transparent
                        px-4
                        pb-5
                        pt-8
                    "
                >
                    <div className="mx-auto max-w-3xl">
                        <InputPrompt
                            thread_id={id}
                            addMessage={addMessage}
                        />
                    </div>
                </div>
            </>
        )}
    </div>
);

}