import { useState } from "react";

import Sidebar from "./components/sidebar/Sidebar"
import Chat from "./components/Chat"
import type { ChatMessages } from "./components/types/ChatMessages";


function App() {

  const [id, setId] = useState<string>("")
  const [messages, setMessages] = useState<ChatMessages[]>([]);

  function changeId(id: string){
    setId(id)
  }

  function changeMessages(message: ChatMessages[] | ChatMessages){
      setMessages( oldMessages => {
          if (Array.isArray(message)) {
              return message;
          }

          return [
              ...oldMessages,
              message
          ];
      })
    }

  return (
    <>
      <Sidebar/>
      <Chat/>
    </>
  )

}

export default App
