import { useState } from 'react'
import { AnimatePresence } from 'framer-motion'
import AnimatedBackground from './components/AnimatedBackground'
import Navbar from './components/Navbar'
import HomePage from './pages/HomePage'
import PredictionsPage from './pages/PredictionsPage'
import DriverAnalysisPage from './pages/DriverAnalysisPage'
import TrainingPage from './pages/TrainingPage'

export default function App() {
  const [page, setPage] = useState('home')
  const [selectedYear, setSelectedYear] = useState(2026)
  const [selectedGP, setSelectedGP] = useState('Bahrain Grand Prix')

  const renderPage = () => {
    switch (page) {
      case 'home':
        return <HomePage onGetStarted={() => setPage('predictions')} />
      case 'predictions':
        return (
          <PredictionsPage
            year={selectedYear}
            gp={selectedGP}
            onYearChange={setSelectedYear}
            onGPChange={setSelectedGP}
          />
        )
      case 'driver-analysis':
        return (
          <DriverAnalysisPage
            year={selectedYear}
            gp={selectedGP}
          />
        )
      case 'training':
        return <TrainingPage />
      default:
        return <HomePage onGetStarted={() => setPage('predictions')} />
    }
  }

  return (
    <div style={{ minHeight: '100vh', position: 'relative' }}>
      <AnimatedBackground />
      <Navbar currentPage={page} onNavigate={setPage} />
      <AnimatePresence mode="wait">
        <div key={page} style={{ position: 'relative', zIndex: 1 }}>
          {renderPage()}
        </div>
      </AnimatePresence>
    </div>
  )
}
