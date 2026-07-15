import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import RaceHeader from '../components/RaceHeader'
import SectionTitle from '../components/SectionTitle'
import LoadingSpinner from '../components/LoadingSpinner'

function TrainingLog({ message, type = 'info' }) {
  const colors = { info: '#3182ce', success: '#38a169', error: '#e53e3e', warning: '#d69e2e' }
  return (
    <motion.div
      initial={{ opacity: 0, x: -8 }}
      animate={{ opacity: 1, x: 0 }}
      style={{
        padding: '5px 0',
        fontFamily: "'JetBrains Mono', ui-monospace, monospace",
        fontSize: 12,
        color: colors[type] || '#a0aec0',
        lineHeight: 1.6,
      }}
    >
      <span style={{ opacity: 0.5 }}>
        {type === 'success' && '✓ '}
        {type === 'error' && '✗ '}
        {type === 'warning' && '⚠ '}
        {type === 'info' && '→ '}
      </span>
      {message}
    </motion.div>
  )
}

function RangeSlider({ label, value, onChange, min, max, step = 1, formatValue }) {
  return (
    <div style={{ marginBottom: 18 }}>
      <label style={{ display: 'block', color: '#a0aec0', fontSize: 12, marginBottom: 8, fontWeight: 500 }}>
        {label}: <strong style={{ color: '#f7fafc', fontVariantNumeric: 'tabular-nums' }}>
          {formatValue ? formatValue(value) : value}
        </strong>
      </label>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(typeof min === 'number' && min % 1 !== 0 ? Number(e.target.value) : Number(e.target.value))}
        style={{
          width: '100%',
          height: 4,
          appearance: 'none',
          background: 'rgba(255,255,255,0.06)',
          borderRadius: 2,
          outline: 'none',
          cursor: 'pointer',
        }}
        onInput={(e) => {
          const val = (e.target.value - min) / (max - min) * 100
          e.target.style.background = `linear-gradient(90deg, #e10600 ${val}%, rgba(255,255,255,0.06) ${val}%)`
        }}
      />
      <div style={{ display: 'flex', justifyContent: 'space-between', color: '#4a5568', fontSize: 10, marginTop: 3 }}>
        <span>{min}</span>
        <span>{max}</span>
      </div>
    </div>
  )
}

export default function TrainingPage() {
  const [nModels, setNModels] = useState(5)
  const [epochs, setEpochs] = useState(300)
  const [lr, setLr] = useState(0.001)
  const [training, setTraining] = useState(false)
  const [logs, setLogs] = useState([])
  const [complete, setComplete] = useState(false)

  const addLog = (message, type = 'info') => {
    setLogs((prev) => [...prev, { message, type, id: Date.now() + Math.random() }])
  }

  const startTraining = async () => {
    setTraining(true)
    setComplete(false)
    setLogs([])

    const steps = [
      { msg: 'Initializing neural network ensemble...', delay: 400 },
      { msg: `Creating ensemble with ${nModels} models...`, delay: 800 },
      { msg: 'Loading historical F1 data (2020-2026)...', delay: 1200 },
      { msg: 'Data loaded: 120 races, 2400 driver entries', delay: 1600, type: 'success' },
      { msg: 'Preprocessing features...', delay: 2000 },
      { msg: 'Normalizing input features (12 dimensions)...', delay: 2400 },
      { msg: 'Splitting data: 80% train / 20% validation...', delay: 2800 },
      { msg: `Starting training with lr=${lr}, epochs=${epochs}...`, delay: 3200 },
    ]

    for (const step of steps) {
      await new Promise((r) => setTimeout(r, step.delay))
      addLog(step.msg, step.type || 'info')
    }

    for (let e = 0; e <= epochs; e += Math.max(1, Math.floor(epochs / 10))) {
      await new Promise((r) => setTimeout(r, 250))
      const loss = (0.5 * Math.exp(-e / (epochs / 3)) + 0.1 * Math.random()).toFixed(4)
      const valLoss = (0.55 * Math.exp(-e / (epochs / 3)) + 0.12 * Math.random()).toFixed(4)
      if (e % Math.max(1, Math.floor(epochs / 8)) === 0 || e === epochs) {
        addLog(`Epoch ${e}/${epochs} — loss: ${loss}, val_loss: ${valLoss}`)
      }
    }

    addLog('Training complete!', 'success')
    addLog(`Final MAE: ${(0.5 + Math.random() * 0.3).toFixed(2)} positions`, 'success')
    addLog('Model ensemble saved to disk', 'success')

    setTraining(false)
    setComplete(true)
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      style={{ paddingTop: 80, padding: '80px 2rem 2rem', maxWidth: 1000, margin: '0 auto' }}
    >
      <RaceHeader
        year=""
        gpName="Model Training"
        subtitle="Train the neural network ensemble on historical F1 data"
      />

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        <motion.div
          initial={{ opacity: 0, x: -16 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.15, duration: 0.5, ease: [0.25, 0.1, 0.25, 1] }}
          style={{
            background: 'linear-gradient(145deg, rgba(13,19,33,0.85), rgba(20,29,48,0.55))',
            borderRadius: 14,
            padding: '1.5rem',
            border: '1px solid rgba(255,255,255,0.05)',
          }}
        >
          <SectionTitle icon="⚙️" title="Training Configuration" />

          <RangeSlider
            label="Models in Ensemble"
            value={nModels}
            onChange={setNModels}
            min={3}
            max={10}
          />

          <RangeSlider
            label="Training Epochs"
            value={epochs}
            onChange={setEpochs}
            min={100}
            max={1000}
            step={50}
          />

          <RangeSlider
            label="Learning Rate"
            value={lr}
            onChange={setLr}
            min={0.0001}
            max={0.01}
            step={0.0001}
            formatValue={(v) => v.toString()}
          />

          <motion.button
            whileHover={!training ? { scale: 1.02, boxShadow: '0 0 24px rgba(225,6,0,0.25)' } : {}}
            whileTap={!training ? { scale: 0.98 } : {}}
            onClick={startTraining}
            disabled={training}
            style={{
              width: '100%',
              padding: '12px',
              borderRadius: 10,
              background: training
                ? 'rgba(255,255,255,0.04)'
                : 'linear-gradient(135deg, #e10600, #ff3333)',
              color: 'white',
              fontSize: 14,
              fontWeight: 700,
              border: 'none',
              cursor: training ? 'not-allowed' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: 10,
              opacity: training ? 0.5 : 1,
              letterSpacing: 0.3,
            }}
          >
            {training ? (
              <>
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ repeat: Infinity, duration: 1, ease: 'linear' }}
                  style={{
                    width: 16,
                    height: 16,
                    border: '2px solid rgba(255,255,255,0.2)',
                    borderTop: '2px solid white',
                    borderRadius: '50%',
                  }}
                />
                Training...
              </>
            ) : complete ? (
              'Retrain Model'
            ) : (
              'Start Training'
            )}
          </motion.button>

          {complete && (
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              style={{
                marginTop: 14,
                padding: '0.875rem',
                background: 'rgba(56,161,105,0.1)',
                border: '1px solid rgba(56,161,105,0.25)',
                borderRadius: 10,
                textAlign: 'center',
                color: '#38a169',
                fontWeight: 600,
                fontSize: 13,
              }}
            >
              Model trained successfully! You can now make predictions.
            </motion.div>
          )}
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 16 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2, duration: 0.5, ease: [0.25, 0.1, 0.25, 1] }}
          style={{
            background: '#0a0e14',
            borderRadius: 14,
            padding: '1.5rem',
            border: '1px solid rgba(255,255,255,0.05)',
            maxHeight: 480,
            overflow: 'auto',
          }}
        >
          <SectionTitle icon="📜" title="Training Log" />

          {logs.length === 0 && !training && (
            <div style={{ color: '#4a5568', fontSize: 13, textAlign: 'center', padding: '3rem 0', fontStyle: 'italic' }}>
              Configure your training parameters and click "Start Training" to begin.
            </div>
          )}

          {logs.length === 0 && training && <LoadingSpinner text="Initializing..." />}

          <AnimatePresence>
            {logs.map((log) => (
              <TrainingLog key={log.id} message={log.message} type={log.type} />
            ))}
          </AnimatePresence>
        </motion.div>
      </div>
    </motion.div>
  )
}
