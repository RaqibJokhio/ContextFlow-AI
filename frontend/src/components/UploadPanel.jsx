import { useState } from 'react'
import { Upload, FileText, Loader2, CheckCircle2, XCircle } from 'lucide-react'

const API_BASE = 'http://127.0.0.1:8000'

function UploadPanel({ uploadedDocs, setUploadedDocs }) {
  const [dragActive, setDragActive] = useState(false)
  const [uploading, setUploading] = useState(false)

  const handleFiles = async (files) => {
    for (const file of files) {
      const docEntry = { name: file.name, status: 'uploading' }
      setUploadedDocs((prev) => [...prev, docEntry])
      setUploading(true)

      const formData = new FormData()
      formData.append('file', file)

      try {
        const res = await fetch(`${API_BASE}/upload`, {
          method: 'POST',
          body: formData
        })

        if (!res.ok) throw new Error('Upload failed')

        const data = await res.json()

        setUploadedDocs((prev) =>
          prev.map((doc) =>
            doc.name === file.name
              ? { ...doc, status: 'done', chunks: data.chunks_created }
              : doc
          )
        )
      } catch (err) {
        setUploadedDocs((prev) =>
          prev.map((doc) =>
            doc.name === file.name ? { ...doc, status: 'error' } : doc
          )
        )
      }
    }
    setUploading(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragActive(false)
    handleFiles(Array.from(e.dataTransfer.files))
  }

  const handleFileInput = (e) => {
    handleFiles(Array.from(e.target.files))
  }

  return (
    <div className="w-full md:w-1/2 p-6 border-b md:border-b-0 md:border-r border-zinc-800">
      <h2 className="text-lg font-semibold mb-4">Upload Documents</h2>

      <div
        onDragOver={(e) => {
          e.preventDefault()
          setDragActive(true)
        }}
        onDragLeave={() => setDragActive(false)}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-2xl p-10 text-center transition-colors ${
          dragActive ? 'border-cyan-400 bg-zinc-900' : 'border-zinc-700'
        }`}
      >
        <Upload className="mx-auto mb-3 text-zinc-400" size={32} />
        <p className="text-zinc-400 mb-3">Drag & drop PDF, DOCX, or TXT files here</p>
        <label className="inline-block cursor-pointer bg-zinc-800 hover:bg-zinc-700 px-4 py-2 rounded-lg text-sm">
          Browse files
          <input
            type="file"
            multiple
            accept=".pdf,.docx,.txt"
            className="hidden"
            onChange={handleFileInput}
          />
        </label>
      </div>

      <div className="mt-6 space-y-2">
        {uploadedDocs.map((doc, i) => (
          <div
            key={i}
            className="flex items-center gap-3 bg-zinc-900 rounded-xl p-3 text-sm"
          >
            <FileText size={18} className="text-zinc-400 shrink-0" />
            <span className="flex-1 truncate">{doc.name}</span>
            {doc.status === 'uploading' && (
              <Loader2 size={18} className="animate-spin text-zinc-400" />
            )}
            {doc.status === 'done' && (
              <CheckCircle2 size={18} className="text-green-400" />
            )}
            {doc.status === 'error' && (
              <XCircle size={18} className="text-red-400" />
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default UploadPanel
