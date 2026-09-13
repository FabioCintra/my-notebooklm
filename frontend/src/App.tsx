import { useState } from "react";

import Sidebar from "./components/sidebar/Sidebar"
import Chat from "./components/Chat"
import type { ChatMessages } from "./components/types/ChatMessages";


function App() {

  const [id, setId] = useState<string>("")

  return (
    <>
      <Sidebar/>
      <Chat/>
    </>
  )

}

export default App
