import { useState, useEffect, createContext } from "react";
import type { ChatContextType } from "./types/ChatContextType";
import type { ChatMessages } from "../components/types/ChatMessages";

export const ChatContext = createContext<ChatContextType>({
    id: "",
    setId: () => {},
    messages: [],
    addMessage: () => {}
})

export default function ChatContextProvider({children}: any) {

    const [id, setId] = useState<string>("");
    const [messages, setMessages] = useState<ChatMessages[]>([]);

    useEffect(() => {
        async function fecthMessagesById(){
            if(id == ""){
                return;
            }

            console.log(id)

            const url = "http://127.0.0.1:8000/notebooks/messages/" + id;
            const json = await fetch(url,
                {
                    method: "GET",
                    credentials: "include"
                }
            );

            const messages: ChatMessages[] = await json.json();
            setMessages(messages)
        }

        fecthMessagesById();

    }, [id])

    function changeId(id: string){
        setId(id)
    }

    function addMessage(msg: ChatMessages){
        setMessages(oldMessages => [
            ...oldMessages,
            msg
        ])
    }

    const ctxValue = {
        id: id,
        setId: changeId,
        messages: messages,
        addMessage: addMessage
    }

    return (
        <ChatContext.Provider value={ctxValue} >
            {children}
        </ChatContext.Provider>
    )
}   