import Sidebar from "./components/sidebar/Sidebar"
import Chat from "./components/chat/Chat"
import ChatContextProvider from "./store/ChatContext";


function App() {
  
  return (
    <ChatContextProvider>
      <div className="flex h-screen w-full">
        <Sidebar />
        <Chat />
      </div>
    </ChatContextProvider>
  )

}

export default App
