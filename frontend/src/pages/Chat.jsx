import { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Link } from 'react-router-dom';
const API_URL = 'http://localhost:8000';

function Chat() {
    const [input, setInput] = useState('');
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const [documents, setDocuments] = useState([]);

    const [sessionId] = useState(() => crypto.randomUUID());

    useEffect(() => {
        const fetchDocuments = async () => {
            try {
                const response = await fetch(`${API_URL}/admin/documents/`);

                if (!response.ok) {
                    throw new Error('Failed to fetch documents');
                }

                const data = await response.json();
                setDocuments(data);
            } catch (error) {
                console.error('Failed to load documents:', error);
            }
        };

        fetchDocuments();
    }, []);

    const sendMessage = async () => {
        if (!input.trim() || loading) return;

        const userMessage = input.trim();

        setMessages((prev) => [
            ...prev,
            {
                role: 'user',
                content: userMessage,
            },
        ]);

        setInput('');
        setLoading(true);

        try {
            const response = await fetch(`${API_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: sessionId,
                    input: userMessage,
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to get response');
            }

            const data = await response.json();

            setMessages((prev) => [
                ...prev,
                {
                    role: 'assistant',
                    content: data.result,
                    sources: data.sources,
                },
            ]);
        } catch (error) {
            setMessages((prev) => [
                ...prev,
                {
                    role: 'assistant',
                    content: 'Something went wrong. Please try again.',
                },
            ]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex h-screen flex-col bg-slate-950 text-white">
            <header className="border-b border-slate-800">
                <div className="relative mx-auto flex w-full max-w-3xl items-center justify-center px-6 py-4">
                    <Link
                        to="/"
                        className="absolute left-6 text-xl text-slate-400 hover:text-white"
                        title="Back to Home"
                    >
                        ←
                    </Link>

                    <div className="text-center">
                        <h1 className="text-lg font-semibold">
                            PolicyBase <span className="text-blue-400">AI</span>
                        </h1>

                        <p className="text-xs text-slate-500">
                            Company Policy Assistant
                        </p>
                    </div>
                </div>
            </header>

            <main className="flex-1 overflow-y-auto">
                <div className="mx-auto w-full max-w-3xl px-6 py-8">
                    {messages.length === 0 ? (
                        <div className="flex h-[60vh] items-center justify-center">
                            <div className="text-center">
                                <div className="mb-4 text-4xl">🤖</div>

                                <h2 className="text-2xl font-semibold">
                                    How can I help you?
                                </h2>

                                <p className="mt-2 text-sm text-slate-500">
                                    Ask me anything about your company policies.
                                </p>
                            </div>
                        </div>
                    ) : (
                        <div className="space-y-6">
                            {messages.map((message, index) => (
                                <div
                                    key={index}
                                    className={
                                        message.role === 'user'
                                            ? 'flex justify-end'
                                            : 'flex justify-start'
                                    }
                                >
                                    <div
                                        className={
                                            message.role === 'user'
                                                ? 'max-w-[80%] rounded-2xl bg-blue-600 px-4 py-3 text-sm'
                                                : 'max-w-[80%] rounded-2xl bg-slate-900 px-4 py-3 text-sm text-slate-200'
                                        }
                                    >
                                        {message.role === 'assistant' ? (
                                            <div className="prose prose-invert max-w-none text-sm">
                                                <ReactMarkdown>
                                                    {message.content}
                                                </ReactMarkdown>
                                            </div>
                                        ) : (
                                            <p className="whitespace-pre-wrap">
                                                {message.content}
                                            </p>
                                        )}

                                        {message.sources?.length > 0 && (
                                            <div className="mt-4 border-t border-slate-700 pt-3">
                                                <p className="mb-2 text-xs font-medium text-slate-500">
                                                    Sources
                                                </p>

                                                {message.sources.map(
                                                    (source, sourceIndex) => (
                                                        <p
                                                            key={sourceIndex}
                                                            className="text-xs text-slate-500"
                                                        >
                                                            📄 {source.filename}{' '}
                                                            — Page {source.page}
                                                        </p>
                                                    ),
                                                )}
                                            </div>
                                        )}
                                    </div>
                                </div>
                            ))}

                            {loading && (
                                <div className="flex justify-start">
                                    <div className="rounded-2xl bg-slate-900 px-4 py-3 text-sm text-slate-500">
                                        Thinking...
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </main>

            <footer className="border-t border-slate-800">
                <div className="mx-auto w-full max-w-3xl px-6 py-5">
                    <div className="flex items-center rounded-2xl border border-slate-700 bg-slate-900 p-2">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter') {
                                    sendMessage();
                                }
                            }}
                            disabled={loading}
                            placeholder="Ask about company policies..."
                            className="flex-1 bg-transparent px-4 py-3 text-sm outline-none placeholder:text-slate-500"
                        />

                        <button
                            onClick={sendMessage}
                            disabled={loading || !input.trim()}
                            className="rounded-xl bg-blue-600 px-5 py-3 text-sm font-medium hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
                        >
                            Send
                        </button>
                    </div>

                    <div className="mt-3 flex flex-wrap justify-center gap-x-3 gap-y-1 text-xs text-slate-600">
                        <span>Answers are based on:</span>

                        {documents.length > 0 ? (
                            documents.map((document) => (
                                <a
                                    key={document.document_id}
                                    href={`${API_URL}/admin/documents/${document.document_id}/file`}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-blue-400 hover:underline"
                                >
                                    📄 {document.filename}
                                </a>
                            ))
                        ) : (
                            <span>available company policy documents</span>
                        )}
                    </div>
                </div>
            </footer>
        </div>
    );
}

export default Chat;
