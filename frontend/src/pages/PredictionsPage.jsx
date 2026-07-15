import { useState, useEffect, useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import RaceHeader from '../components/RaceHeader'
import StatusBanner from '../components/StatusBanner'
import PodiumCard from '../components/PodiumCard'
import MetricCard from '../components/MetricCard'
import SectionTitle from '../components/SectionTitle'
import LoadingSpinner from '../components/LoadingSpinner'
import { getPrediction, TEAM_COLORS, CALENDAR } from '../data/mockData'

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

function Select({ value, onChange, children, minWidth }) {
  return (
    <div style={{ position: 'relative' }}>
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
          minWidth: minWidth || 160,
          appearance: 'none',
          cursor: 'pointer',
          transition: 'border-color 200ms ease',
          outline: 'none',
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

function Table({ headers, rows, renderRow }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: [0.25, 0.1, 0.25, 1] }}
      style={{
        background: 'linear-gradient(145deg, rgba(13,19,33,0.85), rgba(20,29,48,0.55))',
        borderRadius: 12,
        border: '1px solid rgba(255,255,255,0.05)',
        overflow: 'hidden',
        marginBottom: 24,
      }}
    >
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', minWidth: 600 }}>
          <thead>
            <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
              {headers.map((h) => (
                <th
                  key={h}
                  style={{
                    padding: '11px 14px',
                    textAlign: 'left',
                    color: '#a0aec0',
                    fontSize: 11,
                    fontWeight: 600,
                    textTransform: 'uppercase',
                    letterSpacing: 1,
                    whiteSpace: 'nowrap',
                  }}
                >
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>{rows.map((row, i) => renderRow(row, i))}</tbody>
        </table>
      </div>
    </motion.div>
  )
}

function BarChart({ data }) {
  const max = Math.max(...data.map((d) => d.value))
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: [0.25, 0.1, 0.25, 1] }}
      style={{
        background: 'linear-gradient(145deg, rgba(13,19,33,0.85), rgba(20,29,48,0.55))',
        borderRadius: 12,
        border: '1px solid rgba(255,255,255,0.05)',
        padding: '1.5rem',
        marginBottom: 32,
      }}
    >
      {data.map((item, i) => (
        <motion.div
          key={item.name}
          initial={{ opacity: 0, x: -8 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 + i * 0.04, duration: 0.35 }}
          style={{ marginBottom: 6 }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 3 }}>
            <span
              style={{
                width: 120,
                fontSize: 12,
                color: TEAM_COLORS[item.name] || '#a0aec0',
                fontWeight: 500,
                textAlign: 'right',
                flexShrink: 0,
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap',
              }}
            >
              {item.name}
            </span>
            <div
              style={{
                flex: 1,
                height: 22,
                background: 'rgba(255,255,255,0.03)',
                borderRadius: 5,
                overflow: 'hidden',
                position: 'relative',
              }}
            >
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${(item.value / max) * 100}%` }}
                transition={{ delay: 0.4 + i * 0.04, duration: 1, ease: 'easeOut' }}
                style={{
                  height: '100%',
                  background: `linear-gradient(90deg, ${TEAM_COLORS[item.name] || '#666'}, ${TEAM_COLORS[item.name] || '#666'}33)`,
                  borderRadius: 5,
                  display: 'flex',
                  alignItems: 'center',
                  paddingLeft: 8,
                  minWidth: 30,
                }}
              >
                <span
                  style={{
                    fontSize: 11,
                    fontWeight: 700,
                    color: 'white',
                    textShadow: '0 1px 3px rgba(0,0,0,0.6)',
                  }}
                >
                  {item.value.toFixed(1)}
                </span>
              </motion.div>
            </div>
          </div>
        </motion.div>
      ))}
    </motion.div>
  )
}

export default function PredictionsPage({ year, gp, onYearChange, onGPChange }) {
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState(null)

  useEffect(() => {
    setLoading(true)
    const timer = setTimeout(() => {
      setData(getPrediction(year, gp))
      setLoading(false)
    }, 1000)
    return () => clearTimeout(timer)
  }, [year, gp])

  const raceDate = useMemo(() => {
    const dates = { 2024: 'March 2, 2024', 2025: 'April 13, 2025', 2026: 'April 19, 2026' }
    return dates[year] || 'TBD'
  }, [year])

  if (loading) return <div style={{ paddingTop: 80 }}><LoadingSpinner text="Generating predictions..." /></div>

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      style={{ paddingTop: 80, padding: '80px 2rem 2rem', maxWidth: 1200, margin: '0 auto' }}
    >
      <motion.div
        variants={itemVariants}
        style={{
          display: 'flex',
          gap: 12,
          marginBottom: 24,
          flexWrap: 'wrap',
          alignItems: 'center',
          background: 'rgba(13,19,33,0.6)',
          borderRadius: 10,
          padding: '0.875rem 1.25rem',
          border: '1px solid rgba(255,255,255,0.04)',
          backdropFilter: 'blur(8px)',
        }}
      >
        <Select value={year} onChange={(e) => onYearChange(Number(e.target.value))} minWidth={140}>
          {[2024, 2025, 2026].map((y) => (
            <option key={y} value={y}>{y} Season</option>
          ))}
        </Select>
        <Select value={gp} onChange={(e) => onGPChange(e.target.value)} minWidth={220}>
          {(CALENDAR[year] || []).map((g) => (
            <option key={g} value={g}>{g}</option>
          ))}
        </Select>
      </motion.div>

      <RaceHeader year={year} gpName={gp} subtitle="Neural network ensemble predictions with uncertainty estimation" />
      <StatusBanner isPast={data.isPast} raceDate={raceDate} />

      <AnimatePresence>
        {data.isPast && data.actualResults && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.4, ease: [0.25, 0.1, 0.25, 1] }}
          >
            <SectionTitle icon="🏆" title="Actual Podium" delay={0.1} />
            <div style={{ display: 'flex', gap: 14, justifyContent: 'center', flexWrap: 'wrap', marginBottom: 14 }}>
              {data.actualResults.slice(0, 3).map((driver, i) => (
                <PodiumCard
                  key={driver.driver}
                  driverName={driver.driverName}
                  team={driver.team}
                  position={i + 1}
                  tag="ACTUAL"
                  delay={0.2 + i * 0.08}
                />
              ))}
            </div>

            {data.accuracy && (
              <>
                <SectionTitle icon="📊" title="Prediction Accuracy" delay={0.25} />
                <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', marginBottom: 20 }}>
                  <MetricCard label="Avg Position Error" value={data.accuracy.mae} color="#3182ce" delay={0.25} />
                  <MetricCard label="Within 3 Positions" value={data.accuracy.closeMatches} color="#38a169" delay={0.3} />
                  <MetricCard label="Podium Correct" value={data.accuracy.podiumAccuracy} color="#f0b429" delay={0.35} />
                  <MetricCard label="Exact Positions" value={data.accuracy.exactMatches} color="#ff4444" delay={0.4} decimal={0} />
                </div>
              </>
            )}

            <SectionTitle icon="📋" title="Predicted vs Actual Standings" delay={0.35} />
            <Table
              headers={['#', 'Driver', 'Team', 'Actual', 'Predicted', 'Delta']}
              rows={data.comparison}
              renderRow={(row, i) => (
                <motion.tr
                  key={row.driver}
                  initial={{ opacity: 0, x: -8 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.4 + i * 0.025, duration: 0.25 }}
                  style={{
                    borderBottom: '1px solid rgba(255,255,255,0.03)',
                    background: i % 2 === 0 ? 'rgba(255,255,255,0.015)' : 'transparent',
                  }}
                >
                  <td style={{ padding: '9px 14px', color: '#a0aec0', fontSize: 13 }}>{i + 1}</td>
                  <td style={{ padding: '9px 14px', fontWeight: 600, fontSize: 13 }}>{row.driverName}</td>
                  <td style={{ padding: '9px 14px', color: TEAM_COLORS[row.team] || '#666', fontSize: 12 }}>{row.team}</td>
                  <td style={{ padding: '9px 14px', fontSize: 13 }}>{row.actual}</td>
                  <td style={{ padding: '9px 14px', fontSize: 13 }}>{row.predicted}</td>
                  <td
                    style={{
                      padding: '9px 14px',
                      fontSize: 13,
                      fontWeight: 600,
                      color: row.delta < 0 ? '#38a169' : row.delta > 0 ? '#e53e3e' : '#a0aec0',
                    }}
                  >
                    {row.delta > 0 ? '+' : ''}{row.delta}
                  </td>
                </motion.tr>
              )}
            />
          </motion.div>
        )}
      </AnimatePresence>

      <SectionTitle icon="🔮" title="Predicted Podium" />
      <div style={{ display: 'flex', gap: 14, justifyContent: 'center', flexWrap: 'wrap', marginBottom: 20 }}>
        {data.predictions.slice(0, 3).map((driver, i) => (
          <PodiumCard
            key={driver.driver}
            driverName={driver.driverName}
            team={driver.team}
            position={i + 1}
            confidence={driver.confidence}
            tag="PREDICTED"
            delay={0.1 + i * 0.08}
          />
        ))}
      </div>

      <SectionTitle icon="📊" title="Full Predicted Grid" />
      <Table
        headers={['#', 'Driver', 'Team', 'Predicted Pos', 'Uncertainty', 'Confidence']}
        rows={data.predictions}
        renderRow={(row, i) => (
          <motion.tr
            key={row.driver}
            initial={{ opacity: 0, x: -8 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 + i * 0.018, duration: 0.25 }}
            style={{
              borderBottom: '1px solid rgba(255,255,255,0.03)',
              background: i % 2 === 0 ? 'rgba(255,255,255,0.015)' : 'transparent',
            }}
          >
            <td style={{ padding: '9px 14px', color: '#a0aec0', fontSize: 13 }}>{i + 1}</td>
            <td style={{ padding: '9px 14px', fontWeight: 600, fontSize: 13 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <span>{row.driverName}</span>
                <span style={{ color: '#4a5568', fontSize: 11, fontWeight: 400 }}>{row.driver}</span>
              </div>
            </td>
            <td style={{ padding: '9px 14px', color: TEAM_COLORS[row.team] || '#666', fontSize: 12 }}>{row.team}</td>
            <td style={{ padding: '9px 14px', fontWeight: 700, fontSize: 14 }}>{row.predictedPosition}</td>
            <td style={{ padding: '9px 14px', color: '#d69e2e', fontSize: 13 }}>±{row.uncertainty}</td>
            <td style={{ padding: '9px 14px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <div style={{ width: 56, height: 5, background: 'rgba(255,255,255,0.04)', borderRadius: 3, overflow: 'hidden' }}>
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${row.confidence * 100}%` }}
                    transition={{ delay: 0.3 + i * 0.018, duration: 0.8, ease: 'easeOut' }}
                    style={{
                      height: '100%',
                      background: `linear-gradient(90deg, ${row.confidence > 0.85 ? '#38a169' : row.confidence > 0.75 ? '#d69e2e' : '#e53e3e'}, ${row.confidence > 0.85 ? '#38a16966' : row.confidence > 0.75 ? '#d69e2e66' : '#e53e3e66'})`,
                      borderRadius: 3,
                    }}
                  />
                </div>
                <span style={{ fontSize: 12, color: '#a0aec0', fontVariantNumeric: 'tabular-nums' }}>
                  {(row.confidence * 100).toFixed(0)}%
                </span>
              </div>
            </td>
          </motion.tr>
        )}
      />

      <SectionTitle icon="🏢" title="Team Average Predicted Position" />
      {(() => {
        const teams = {}
        data.predictions.forEach((p) => {
          if (!teams[p.team]) teams[p.team] = []
          teams[p.team].push(p.predictedPosition)
        })
        const sorted = Object.entries(teams)
          .map(([name, pos]) => ({ name, value: pos.reduce((a, b) => a + b, 0) / pos.length }))
          .sort((a, b) => a.value - b.value)
        return <BarChart data={sorted} colorKey="team" />
      })()}
    </motion.div>
  )
}
