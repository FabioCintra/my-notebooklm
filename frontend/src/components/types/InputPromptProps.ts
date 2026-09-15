import type { ChatMessages } from "./ChatMessages"

export type InputPromptProps = {
    thread_id: string,
    addMessage: (message: ChatMessages) => void
}