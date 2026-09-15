import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
const API_URL = 'https://policybase-ai-api.vercel.app';

function Admin() {
    const [documents, setDocuments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [authenticated, setAuthenticated] = useState(false);
    const [uploading, setUploading] = useState(false);

    useEffect(() => {
        const authenticate = async () => {
            const password = window.prompt('Enter admin password');

            if (!password) {
                window.location.href = '/';
                return;
            }

            try {
                const response = await fetch(`${API_URL}/admin/auth`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        password,
                    }),
                });

                if (!response.ok) {
                    alert('Invalid admin password');
                    window.location.href = '/';
                    return;
                }

                setAuthenticated(true);
                fetchDocuments();
            } catch {
                alert('Unable to authenticate');
                window.location.href = '/';
            }
        };

        authenticate();
    }, []);

    const fetchDocuments = async () => {
        try {
            const response = await fetch(`${API_URL}/admin/documents/`);

            if (!response.ok) {
                throw new Error('Failed to fetch documents');
            }

            const data = await response.json();
            setDocuments(data);
        } catch (error) {
            console.error(error);
            alert('Failed to load documents');
        } finally {
            setLoading(false);
        }
    };

    const uploadDocument = async (event) => {
        const file = event.target.files[0];

        if (!file) return;

        setUploading(true);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${API_URL}/admin/documents/upload`, {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Upload failed');
            }

            alert('Document uploaded successfully');

            // Refresh list
            await fetchDocuments();
        } catch (error) {
            alert(error.message);
        } finally {
            setUploading(false);

            // Allow uploading the same filename again after deletion
            event.target.value = '';
        }
    };

    const deleteDocument = async (documentId, filename) => {
        const confirmed = window.confirm(
            `Are you sure you want to delete "${filename}"?`,
        );

        if (!confirmed) return;

        try {
            const response = await fetch(
                `${API_URL}/admin/documents/${documentId}`,
                {
                    method: 'DELETE',
                },
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Delete failed');
            }

            // Remove immediately from UI
            setDocuments((prev) =>
                prev.filter((document) => document.document_id !== documentId),
            );
        } catch (error) {
            alert(error.message);
        }
    };

    return (
        <div className="min-h-screen bg-slate-950 text-white">
            <header className="border-b border-slate-800">
                <div className="relative mx-auto flex w-full max-w-5xl items-center justify-center px-6 py-4">
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

            {authenticated ? (
                <main className="mx-auto max-w-5xl px-6 py-10">
                    <section>
                        <h2 className="text-lg font-semibold">
                            Upload Policy Document
                        </h2>

                        <p className="mt-1 text-sm text-slate-500">
                            Upload a PDF policy document to add it to the
                            knowledge base.
                        </p>

                        <div className="mt-5">
                            <input
                                type="file"
                                accept=".pdf,application/pdf"
                                onChange={uploadDocument}
                                disabled={uploading}
                                className="block w-full cursor-pointer rounded-xl border border-slate-700 bg-slate-900 p-3 text-sm text-slate-300 file:mr-4 file:rounded-lg file:border-0 file:bg-blue-600 file:px-4 file:py-2 file:text-sm file:font-medium file:text-white hover:file:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
                            />
                        </div>

                        {uploading && (
                            <p className="mt-3 text-sm text-blue-400">
                                Uploading and indexing document...
                            </p>
                        )}
                    </section>

                    <section className="mt-12">
                        <div className="flex items-center justify-between">
                            <h2 className="text-lg font-semibold">
                                Available Documents
                            </h2>

                            <span className="text-sm text-slate-500">
                                {documents.length} document
                                {documents.length !== 1 ? 's' : ''}
                            </span>
                        </div>

                        {loading ? (
                            <p className="mt-5 text-sm text-slate-500">
                                Loading documents...
                            </p>
                        ) : documents.length === 0 ? (
                            <div className="mt-5 rounded-xl border border-dashed border-slate-700 p-8 text-center">
                                <p className="text-sm text-slate-500">
                                    No policy documents available.
                                </p>
                            </div>
                        ) : (
                            <div className="mt-5 space-y-3">
                                {documents.map((document) => (
                                    <div
                                        key={document.document_id}
                                        className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-900 px-5 py-4"
                                    >
                                        <div className="flex items-center gap-4">
                                            <div className="text-2xl">📄</div>

                                            <div>
                                                <p className="text-sm font-medium">
                                                    {document.filename}
                                                </p>

                                                <p className="mt-1 text-xs text-slate-500">
                                                    Status: {document.status}
                                                </p>
                                            </div>
                                        </div>

                                        <div className="flex items-center gap-3">
                                            <a
                                                href={`${API_URL}/admin/documents/${document.document_id}/file`}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="rounded-lg border border-slate-700 px-3 py-2 text-xs text-slate-300 hover:bg-slate-800"
                                            >
                                                View
                                            </a>

                                            <button
                                                onClick={() =>
                                                    deleteDocument(
                                                        document.document_id,
                                                        document.filename,
                                                    )
                                                }
                                                className="rounded-lg border border-red-900 px-3 py-2 text-xs text-red-400 hover:bg-red-950"
                                            >
                                                Delete
                                            </button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </section>
                </main>
            ) : (
                <h1></h1>
            )}
        </div>
    );
}

export default Admin;
