import { Link } from 'react-router-dom';

function Home() {
    return (
        <div className="min-h-screen bg-slate-950 text-white">
            <main className="flex min-h-[calc(100vh-81px)] items-center justify-center px-6">
                <div className="max-w-3xl text-center">
                    <p className="mb-6 text-blue-400">
                        AI-Powered Policy Assistant
                    </p>

                    <h1 className="text-5xl font-bold">
                        Your company policies,
                        <span className="text-blue-400"> simplified.</span>
                    </h1>

                    <p className="mx-auto mt-6 max-w-2xl text-lg text-slate-400">
                        Ask questions about company policies and get clear,
                        document-backed answers.
                    </p>
                    <div className="mt-6 flex gap-3 items-center justify-center">
                        <Link
                            to="/chat"
                            className="rounded-lg border border-slate-700 px-4 py-2 text-sm hover:bg-slate-800"
                        >
                            🤖 Ask a Question
                        </Link>

                        <Link
                            to="/admin"
                            className="rounded-lg border border-slate-700 px-4 py-2 text-sm hover:bg-slate-800"
                        >
                            🔐 Admin
                        </Link>
                    </div>
                </div>
            </main>
        </div>
    );
}
export default Home;
