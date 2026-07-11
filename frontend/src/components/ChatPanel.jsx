import { useState, useRef, useEffect } from 'react'
import { Send, Loader2, FileText } from 'lucide-react'

const API_BASE = 'http://127.0.0.1:8000'

function ChatPanel() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async () => {
    const question = input.trim()
    if (!question || loading) return

    setMessages((prev) => [...prev, { role: 'user', text: question }])
    setInput('')
    setLoading(true)

    try {
      const res = await fetch(`${API_BASE}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, top_k: 3 })
      })

      if (!res.ok) throw new Error('Query failed')

      const data = await res.json()

      setMessages((prev) => [
        ...prev,
        { role: 'assistant', text: data.answer, sources: data.sources }
      ])
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', text: 'Something went wrong. Please try again.', sources: [] }
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="w-full md:w-1/2 p-6 flex flex-col h-screen">
      <h2 className="text-lg font-semibold mb-4">Ask Your Documents</h2>

      <div className="flex-1 overflow-y-auto space-y-4 mb-4">
        {messages.length === 0 && (
          <p className="text-zinc-500 text-sm">
            Upload a document on the left, then ask a question about it here.
          </p>
        )}

        {messages.map((msg, i) => (
          <div
            key={i}
            className={`rounded-2xl p-4 text-sm max-w-[90%] ${
              msg.role === 'user'
                ? 'bg-cyan-900/30 ml-auto text-right'
                : 'bg-zinc-900'
            }`}
          >
            <p>{msg.text}</p>

            {msg.sources && msg.sources.length > 0 && (
              <div className="mt-3 flex flex-wrap gap-2 justify-start">
                {msg.sources.map((src, j) => (
                  <span
                    key={j}
                    className="flex items-center gap-1 bg-zinc-800 text-zinc-400 text-xs px-2 py-1 rounded-full"
                  >
                    <FileText size={12} />
                    {src.source} · {src.score}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="bg-zinc-900 rounded-2xl p-4 text-sm flex items-center gap-2 text-zinc-400">
            <Loader2 size={16} className="animate-spin" />
            Thinking...
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <div className="flex gap-2">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about your documents..."
          rows={1}
          className="flex-1 bg-zinc-900 rounded-xl px-4 py-3 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-cyan-500"
        />
        <button
          onClick={handleSend}
          disabled={loading}
          className="bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 rounded-xl px-4 flex items-center justify-center"
        >
          <Send size={18} />
        </button>
      </div>
    </div>
  )
}

export default ChatPanel