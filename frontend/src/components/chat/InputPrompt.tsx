import { useEffect, useState, useRef } from "react";
import type { MessageRequest } from "../types/MessageRequest";
import type { MessageResponse } from "../types/MessageResponse";
import type { ChatMessages } from "../types/ChatMessages";
import type { InputPromptProps } from "../types/InputPromptProps";

export default function InputPrompt({thread_id, addMessage}: InputPromptProps){
    
    const [prompt, setPrompt] = useState("");
    const [isGenerating, setIsGenerating] = useState(false);

    const textareaRef = useRef<HTMLTextAreaElement>(null);

    useEffect(() => {
        const textarea = textareaRef.current;

        if (!textarea) return;

        textarea.style.height = "auto";

        textarea.style.height =
            Math.min(textarea.scrollHeight, 180) + "px";
    }, [prompt]);

    async function handleSend() {
        if (!prompt.trim() || isGenerating) return;

        setIsGenerating(true);

        try {
            const body :MessageRequest = {
                thread_id: thread_id,
                prompt: prompt
            }

            const newMessageHuman: ChatMessages = {
                identifier: "Human",
                message: prompt
            }
            addMessage(newMessageHuman)
            setPrompt("");

            const result = await fetch("http://127.0.0.1:8000/llms/",
                {
                    method: "POST",
                    credentials: "include",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(body)
                }
            );

            const response: MessageResponse = await result.json()
            const newMessageAI: ChatMessages = {
                identifier: "AI",
                message: response.answer
            }
            addMessage(newMessageAI)

        } finally {
            setIsGenerating(false);
        }
    }

    return (
        <div className="w-full px-4 pb-4">
            <div
                className="
                    mx-auto
                    flex
                    max-w-3xl
                    items-end
                    gap-2
                    rounded-3xl
                    border
                    border-gray-300
                    bg-white
                    px-4
                    py-3
                    shadow-sm
                    transition
                    focus-within:border-gray-400
                "
            >
                <textarea
                    ref={textareaRef}
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="Pergunte alguma coisa..."
                    rows={1}
                    className="
                        max-h-[180px]
                        min-h-[24px]
                        flex-1
                        resize-none
                        overflow-y-auto
                        bg-transparent
                        text-[15px]
                        leading-6
                        text-gray-900
                        outline-none
                        placeholder:text-gray-400
                    "
                />

                <button
                    onClick={handleSend}
                    disabled={!prompt.trim() && !isGenerating}
                    className="
                        flex
                        h-9
                        w-9
                        shrink-0
                        items-center
                        justify-center
                        rounded-full
                        bg-black
                        text-white
                        transition
                        hover:bg-gray-800
                        disabled:bg-gray-300
                    "
                >
                    {isGenerating ? (
                        <span className="h-3 w-3 rounded-sm bg-white" />
                    ) : (
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2.5"
                            className="h-5 w-5"
                        >
                            <path d="M12 19V5" />
                            <path d="M6 11l6-6 6 6" />
                        </svg>
                    )}
                </button>
            </div>
        </div>
    );
}
