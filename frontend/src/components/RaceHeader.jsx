import { motion } from 'framer-motion'

export default function RaceHeader({ year, gpName, subtitle }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: -16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: [0.25, 0.1, 0.25, 1] }}
      style={{
        background: 'linear-gradient(135deg, #0d1321 0%, #141d30 50%, #1a2338 100%)',
        borderRadius: 14,
        padding: '1.75rem 2.25rem',
        marginBottom: 24,
        border: '1px solid rgba(255,255,255,0.06)',
        boxShadow: '0 4px 24px rgba(0,0,0,0.4)',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      <div
        style={{
          position: 'absolute',
          top: 0,
          right: 0,
          width: 240,
          height: 240,
          background: 'radial-gradient(circle, rgba(225,6,0,0.06) 0%, transparent 70%)',
          borderRadius: '50%',
          transform: 'translate(30%, -30%)',
        }}
      />
      <div
        style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          width: 160,
          height: 160,
          background: 'radial-gradient(circle, rgba(255,255,255,0.02) 0%, transparent 70%)',
          borderRadius: '50%',
          transform: 'translate(-30%, 30%)',
        }}
      />

      <motion.h1
        initial={{ opacity: 0, x: -16 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.1, duration: 0.5 }}
        style={{
          fontFamily: "'Orbitron', monospace",
          fontSize: 24,
          fontWeight: 800,
          background: 'linear-gradient(90deg, #e10600, #ff4444, #ff6b6b)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          marginBottom: 4,
          position: 'relative',
          zIndex: 1,
          lineHeight: 1.2,
        }}
      >
        {gpName} {year}
      </motion.h1>
      {subtitle && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          style={{
            color: '#a0aec0',
            fontSize: 14,
            fontWeight: 400,
            position: 'relative',
            zIndex: 1,
          }}
        >
          {subtitle}
        </motion.p>
      )}
    </motion.div>
  )
}
