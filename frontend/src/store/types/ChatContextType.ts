import type { ChatMessages } from "../../components/types/ChatMessages";

export interface ChatContextType {
    id: string;
    setId: (id: string) => void;

    messages: ChatMessages[];
    addMessage: (message: ChatMessages) => void;
}