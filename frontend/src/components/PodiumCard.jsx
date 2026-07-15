import { motion } from 'framer-motion'
import { TEAM_COLORS } from '../data/mockData'

const podiumStyles = {
  1: {
    borderColor: '#f0b429',
    color: '#f0b429',
    translateY: 0,
    scale: 1.04,
    label: 'P1',
    gradient: 'linear-gradient(145deg, rgba(240,180,41,0.1), rgba(240,180,41,0.02))',
    glow: '0 0 30px rgba(240,180,41,0.15)',
  },
  2: {
    borderColor: '#a0aec0',
    color: '#a0aec0',
    translateY: 8,
    scale: 1,
    label: 'P2',
    gradient: 'linear-gradient(145deg, rgba(160,174,192,0.08), rgba(160,174,192,0.02))',
    glow: '0 0 20px rgba(160,174,192,0.1)',
  },
  3: {
    borderColor: '#c47b3c',
    color: '#c47b3c',
    translateY: 16,
    scale: 0.96,
    label: 'P3',
    gradient: 'linear-gradient(145deg, rgba(196,123,60,0.08), rgba(196,123,60,0.02))',
    glow: '0 0 20px rgba(196,123,60,0.1)',
  },
}

export default function PodiumCard({
  driverName,
  team,
  position,
  confidence,
  tag = 'PREDICTED',
  delay = 0,
}) {
  const style = podiumStyles[position] || podiumStyles[3]
  const teamColor = TEAM_COLORS[team] || '#666'
  const isActual = tag === 'ACTUAL'

  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: style.translateY }}
      transition={{ delay, duration: 0.5, ease: [0.25, 0.1, 0.25, 1] }}
      whileHover={{
        y: style.translateY - 6,
        scale: 1.02,
        boxShadow: '0 12px 40px rgba(0,0,0,0.6)',
        transition: { duration: 0.2 },
      }}
      style={{
        background: 'linear-gradient(145deg, rgba(13,19,33,0.85), rgba(20,29,48,0.55))',
        borderRadius: 14,
        padding: '1.5rem 1.25rem',
        textAlign: 'center',
        borderTop: `3px solid ${style.borderColor}`,
        boxShadow: `0 4px 24px rgba(0,0,0,0.4), ${style.glow}`,
        position: 'relative',
        overflow: 'hidden',
        flex: 1,
        maxWidth: 250,
        minWidth: 180,
      }}
    >
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: style.gradient,
          pointerEvents: 'none',
        }}
      />

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: delay + 0.15, duration: 0.3 }}
        style={{
          fontSize: 10,
          fontWeight: 700,
          textTransform: 'uppercase',
          letterSpacing: 2.5,
          color: isActual ? '#38a169' : '#3182ce',
          marginBottom: 10,
          position: 'relative',
          zIndex: 1,
        }}
      >
        {tag}
      </motion.div>

      <motion.div
        initial={{ opacity: 0, scale: 0.7 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: delay + 0.1, type: 'spring', stiffness: 250, damping: 15 }}
        style={{
          fontSize: 30,
          fontWeight: 900,
          color: style.color,
          marginBottom: 6,
          position: 'relative',
          zIndex: 1,
          lineHeight: 1,
        }}
      >
        {style.label}
      </motion.div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: delay + 0.25, duration: 0.3 }}
        style={{
          fontSize: 16,
          fontWeight: 700,
          color: '#f7fafc',
          marginBottom: 4,
          position: 'relative',
          zIndex: 1,
        }}
      >
        {driverName}
      </motion.div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: delay + 0.35, duration: 0.3 }}
        style={{
          fontSize: 12,
          color: teamColor,
          marginBottom: 6,
          position: 'relative',
          zIndex: 1,
          fontWeight: 500,
        }}
      >
        {team}
      </motion.div>

      {confidence && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: delay + 0.45, duration: 0.3 }}
          style={{
            position: 'relative',
            zIndex: 1,
            marginTop: 8,
          }}
        >
          <div
            style={{
              height: 3,
              background: 'rgba(255,255,255,0.05)',
              borderRadius: 2,
              overflow: 'hidden',
              width: '80%',
              margin: '0 auto',
            }}
          >
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${confidence * 100}%` }}
              transition={{ delay: delay + 0.6, duration: 1, ease: 'easeOut' }}
              style={{
                height: '100%',
                background: `linear-gradient(90deg, ${style.borderColor}, ${style.borderColor}66)`,
                borderRadius: 2,
              }}
            />
          </div>
          <div style={{ fontSize: 11, color: '#a0aec0', marginTop: 4 }}>
            {(confidence * 100).toFixed(0)}% confidence
          </div>
        </motion.div>
      )}
    </motion.div>
  )
}
