import type { ChatMessages } from "../types/ChatMessages";

export default function Messages({identifier, message}: ChatMessages){

    const isHuman = identifier === "Human";

    return (
        <div
            className={`
                flex w-full
                ${isHuman ? "justify-end" : "justify-start"}
            `}
        >
            <div
                className={`
                    max-w-[70%]
                    rounded-2xl
                    px-4 py-2
                    break-words
                    whitespace-pre-wrap
                    ${
                        isHuman
                            ? "bg-gray-200 text-gray-900"
                            : "bg-gray-100 text-gray-900"
                    }
                `}
            >
                {message}
            </div>
        </div>
    );

}