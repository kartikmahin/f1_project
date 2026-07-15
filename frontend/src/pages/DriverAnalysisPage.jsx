import { useState, useEffect, useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import RaceHeader from '../components/RaceHeader'
import LoadingSpinner from '../components/LoadingSpinner'
import { getPrediction, getDriverData, TEAM_COLORS, DRIVERS_2026 } from '../data/mockData'

function RadarChart({ data, labels, color }) {
  const size = 260
  const center = size / 2
  const radius = 100
  const angleStep = (Math.PI * 2) / labels.length

  const points = data.map((val, i) => {
    const angle = -Math.PI / 2 + i * angleStep
    return {
      x: center + radius * val * Math.cos(angle),
      y: center + radius * val * Math.sin(angle),
    }
  })

  const gridLevels = [0.2, 0.4, 0.6, 0.8, 1.0]

  return (
    <svg width={size} height={size} style={{ display: 'block', margin: '0 auto' }} aria-label="Radar chart">
      {gridLevels.map((level) => {
        const gridPoints = labels.map((_, i) => {
          const angle = -Math.PI / 2 + i * angleStep
          return {
            x: center + radius * level * Math.cos(angle),
            y: center + radius * level * Math.sin(angle),
          }
        })
        return (
          <polygon
            key={level}
            points={gridPoints.map((p) => `${p.x},${p.y}`).join(' ')}
            fill="none"
            stroke="rgba(255,255,255,0.05)"
            strokeWidth={0.5}
          />
        )
      })}

      {labels.map((_, i) => {
        const angle = -Math.PI / 2 + i * angleStep
        return (
          <line
            key={i}
            x1={center}
            y1={center}
            x2={center + radius * Math.cos(angle)}
            y2={center + radius * Math.sin(angle)}
            stroke="rgba(255,255,255,0.05)"
            strokeWidth={0.5}
          />
        )
      })}

      {labels.map((label, i) => {
        const angle = -Math.PI / 2 + i * angleStep
        const labelRadius = radius + 20
        const x = center + labelRadius * Math.cos(angle)
        const y = center + labelRadius * Math.sin(angle)
        return (
          <text
            key={i}
            x={x}
            y={y}
            textAnchor="middle"
            dominantBaseline="middle"
            fill="#a0aec0"
            fontSize={8}
            fontWeight={500}
          >
            {label}
          </text>
        )
      })}

      <motion.polygon
        initial={{ opacity: 0, scale: 0.6 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8, ease: [0.25, 0.1, 0.25, 1] }}
        points={points.map((p) => `${p.x},${p.y}`).join(' ')}
        fill={`${color}22`}
        stroke={color}
        strokeWidth={1.5}
      />

      {points.map((p, i) => (
        <motion.circle
          key={i}
          initial={{ r: 0 }}
          animate={{ r: 3.5 }}
          transition={{ delay: 0.4 + i * 0.08, duration: 0.3 }}
          cx={p.x}
          cy={p.y}
          fill={color}
          stroke="white"
          strokeWidth={1.2}
        />
      ))}
    </svg>
  )
}

function Select({ value, onChange, children }) {
  return (
    <div style={{ position: 'relative', display: 'inline-block' }}>
      <select
        value={value}
        onChange={onChange}
        style={{
          background: 'rgba(255,255,255,0.04)',
          color: '#f7fafc',
          border: '1px solid rgba(255,255,255,0.08)',
          borderRadius: 8,
          padding: '8px 32px 8px 12px',
          fontSize: 13,
          fontWeight: 500,
          minWidth: 240,
          appearance: 'none',
          cursor: 'pointer',
          outline: 'none',
          transition: 'border-color 200ms ease',
        }}
        onFocus={(e) => (e.target.style.borderColor = 'rgba(225,6,0,0.4)')}
        onBlur={(e) => (e.target.style.borderColor = 'rgba(255,255,255,0.08)')}
      >
        {children}
      </select>
      <div
        style={{
          position: 'absolute',
          right: 12,
          top: '50%',
          transform: 'translateY(-50%)',
          color: '#a0aec0',
          fontSize: 9,
          pointerEvents: 'none',
        }}
      >
        ▼
      </div>
    </div>
  )
}

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.06, delayChildren: 0.05 },
  },
}

const itemVariants = {
  hidden: { opacity: 0, y: 12 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.4, ease: [0.25, 0.1, 0.25, 1] },
  },
}

export default function DriverAnalysisPage({ year, gp }) {
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState(null)
  const [selectedDriver, setSelectedDriver] = useState('VER')

  useEffect(() => {
    setLoading(true)
    setSelectedDriver('VER')
    const timer = setTimeout(() => {
      setData(getPrediction(year, gp))
      setLoading(false)
    }, 700)
    return () => clearTimeout(timer)
  }, [year, gp])

  const driverInfo = DRIVERS_2026[selectedDriver]

  const driverFeatures = useMemo(() => {
    if (!selectedDriver) return null
    return getDriverData(selectedDriver)
  }, [selectedDriver])

  const featureLabels = useMemo(() => {
    if (!driverFeatures) return []
    return Object.keys(driverFeatures).map(
      (k) => k.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())
    )
  }, [driverFeatures])

  const featureValues = useMemo(() => {
    if (!driverFeatures) return []
    const vals = Object.values(driverFeatures)
    const max = Math.max(...vals)
    return vals.map((v) => v / max)
  }, [driverFeatures])

  if (loading) return <div style={{ paddingTop: 80 }}><LoadingSpinner text="Loading driver data..." /></div>

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      style={{ paddingTop: 80, padding: '80px 2rem 2rem', maxWidth: 1200, margin: '0 auto' }}
    >
      <RaceHeader year={year} gpName={gp} subtitle="Driver deep dive with feature analysis" />

      <motion.div
        variants={itemVariants}
        style={{
          background: 'rgba(13,19,33,0.6)',
          borderRadius: 10,
          padding: '0.875rem 1.25rem',
          border: '1px solid rgba(255,255,255,0.04)',
          backdropFilter: 'blur(8px)',
          marginBottom: 24,
          display: 'flex',
          alignItems: 'center',
          gap: 12,
          flexWrap: 'wrap',
        }}
      >
        <label style={{ color: '#a0aec0', fontSize: 13, fontWeight: 500 }}>Select Driver:</label>
        <Select value={selectedDriver} onChange={(e) => setSelectedDriver(e.target.value)}>
          {Object.entries(DRIVERS_2026).map(([code, info]) => (
            <option key={code} value={code}>
              {info.name} ({code}) — {info.team}
            </option>
          ))}
        </Select>
      </motion.div>

      <AnimatePresence mode="wait">
        {driverInfo && (
          <motion.div
            key={selectedDriver}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -16 }}
            transition={{ duration: 0.35, ease: [0.25, 0.1, 0.25, 1] }}
          >
            <motion.div
              variants={itemVariants}
              style={{
                background: `linear-gradient(145deg, rgba(13,19,33,0.85), rgba(20,29,48,0.55))`,
                borderRadius: 14,
                padding: '1.25rem 1.75rem',
                border: `1px solid ${TEAM_COLORS[driverInfo.team] || '#666'}22`,
                marginBottom: 24,
                display: 'flex',
                alignItems: 'center',
                gap: 20,
                flexWrap: 'wrap',
              }}
            >
              <div
                style={{
                  width: 56,
                  height: 56,
                  borderRadius: 14,
                  background: `linear-gradient(135deg, ${TEAM_COLORS[driverInfo.team] || '#666'}22, transparent)`,
                  border: `2px solid ${TEAM_COLORS[driverInfo.team] || '#666'}`,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: 20,
                  fontWeight: 900,
                  color: TEAM_COLORS[driverInfo.team] || '#666',
                  fontFamily: "'Orbitron', monospace",
                  flexShrink: 0,
                }}
              >
                {selectedDriver}
              </div>
              <div>
                <div style={{ fontSize: 20, fontWeight: 700, color: '#f7fafc' }}>{driverInfo.name}</div>
                <div style={{ fontSize: 13, color: TEAM_COLORS[driverInfo.team] || '#666', fontWeight: 500 }}>{driverInfo.team}</div>
              </div>
            </motion.div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginBottom: 24 }}>
              <motion.div
                variants={itemVariants}
                style={{
                  background: 'linear-gradient(145deg, rgba(13,19,33,0.85), rgba(20,29,48,0.55))',
                  borderRadius: 14,
                  padding: '1.5rem',
                  border: '1px solid rgba(255,255,255,0.05)',
                  textAlign: 'center',
                }}
              >
                <h3 style={{ fontSize: 15, fontWeight: 700, color: '#f7fafc', marginBottom: 14 }}>
                  Feature Profile
                </h3>
                {driverFeatures && (
                  <RadarChart
                    data={featureValues}
                    labels={featureLabels.map((l) => {
                      const words = l.split(' ')
                      return words.slice(0, 2).join('\n')
                    })}
                    color={TEAM_COLORS[driverInfo.team] || '#666'}
                  />
                )}
              </motion.div>

              <motion.div
                variants={itemVariants}
                style={{
                  background: 'linear-gradient(145deg, rgba(13,19,33,0.85), rgba(20,29,48,0.55))',
                  borderRadius: 14,
                  padding: '1.5rem',
                  border: '1px solid rgba(255,255,255,0.05)',
                }}
              >
                <h3 style={{ fontSize: 15, fontWeight: 700, color: '#f7fafc', marginBottom: 14 }}>
                  Feature Values
                </h3>
                {driverFeatures && Object.entries(driverFeatures).map(([key, val], i) => (
                  <motion.div
                    key={key}
                    initial={{ opacity: 0, x: -8 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.3 + i * 0.04, duration: 0.3 }}
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      padding: '7px 0',
                      borderBottom: i < Object.keys(driverFeatures).length - 1 ? '1px solid rgba(255,255,255,0.04)' : 'none',
                    }}
                  >
                    <span style={{ color: '#a0aec0', fontSize: 12, textTransform: 'capitalize' }}>
                      {key.replace(/_/g, ' ')}
                    </span>
                    <span style={{ color: '#f7fafc', fontWeight: 700, fontSize: 13, fontVariantNumeric: 'tabular-nums' }}>
                      {typeof val === 'number' ? val.toFixed(2) : val}
                    </span>
                  </motion.div>
                ))}
              </motion.div>
            </div>

            {data && (
              <motion.div
                variants={itemVariants}
                style={{
                  background: 'linear-gradient(145deg, rgba(13,19,33,0.85), rgba(20,29,48,0.55))',
                  borderRadius: 14,
                  padding: '1.5rem',
                  border: '1px solid rgba(255,255,255,0.05)',
                }}
              >
                <h3 style={{ fontSize: 15, fontWeight: 700, color: '#f7fafc', marginBottom: 14 }}>
                  Race Prediction for {gp}
                </h3>
                {(() => {
                  const pred = data.predictions.find((p) => p.driver === selectedDriver)
                  if (!pred) return <p style={{ color: '#a0aec0' }}>No prediction available</p>
                  return (
                    <div style={{ display: 'flex', gap: 14, flexWrap: 'wrap' }}>
                      {[
                        { label: 'Predicted Position', value: `#${pred.predictedPosition}`, color: '#3182ce' },
                        { label: 'Uncertainty', value: `±${pred.uncertainty}`, color: '#d69e2e' },
                        { label: 'Confidence', value: `${(pred.confidence * 100).toFixed(0)}%`, color: '#38a169' },
                      ].map((stat) => (
                        <div
                          key={stat.label}
                          style={{
                            flex: 1,
                            minWidth: 110,
                            background: 'rgba(255,255,255,0.03)',
                            borderRadius: 10,
                            padding: '1rem',
                            textAlign: 'center',
                          }}
                        >
                          <div style={{ fontSize: 22, fontWeight: 800, color: stat.color, marginBottom: 4, lineHeight: 1 }}>
                            {stat.value}
                          </div>
                          <div style={{ fontSize: 10, color: '#a0aec0', textTransform: 'uppercase', letterSpacing: 0.8, fontWeight: 500 }}>
                            {stat.label}
                          </div>
                        </div>
                      ))}
                    </div>
                  )
                })()}
              </motion.div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}
