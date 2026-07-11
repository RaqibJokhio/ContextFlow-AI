import { useState } from 'react'
import UploadPanel from './components/UploadPanel'
import ChatPanel from './components/ChatPanel'

function App() {
  const [uploadedDocs, setUploadedDocs] = useState([])

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 flex flex-col md:flex-row">
      <UploadPanel uploadedDocs={uploadedDocs} setUploadedDocs={setUploadedDocs} />
      <ChatPanel />
    </div>
  )
}

export default App