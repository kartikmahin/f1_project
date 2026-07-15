import { motion } from 'framer-motion'

export default function StatusBanner({ isPast, raceDate }) {
  const bg = isPast
    ? 'linear-gradient(135deg, rgba(56,161,105,0.12) 0%, rgba(56,161,105,0.04) 100%)'
    : 'linear-gradient(135deg, rgba(214,158,46,0.12) 0%, rgba(214,158,46,0.04) 100%)'
  const border = isPast ? 'rgba(56,161,105,0.3)' : 'rgba(214,158,46,0.3)'
  const color = isPast ? '#38a169' : '#d69e2e'

  return (
    <motion.div
      initial={{ opacity: 0, y: 8, scale: 0.98 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.35, ease: [0.25, 0.1, 0.25, 1] }}
      style={{
        background: bg,
        border: `1px solid ${border}`,
        borderRadius: 10,
        padding: '0.875rem 1.25rem',
        marginBottom: 24,
        color,
        fontWeight: 500,
        fontSize: 13,
        display: 'flex',
        alignItems: 'center',
        gap: 10,
      }}
    >
      <motion.span
        animate={{ rotate: [0, 8, -8, 0] }}
        transition={{ repeat: Infinity, duration: 3, ease: 'easeInOut' }}
        style={{ fontSize: 16, flexShrink: 0 }}
      >
        {isPast ? '✓' : '○'}
      </motion.span>
      <span>
        {isPast
          ? 'This race has already happened — showing actual results alongside predictions for comparison.'
          : `This race hasn't happened yet (scheduled: ${raceDate}) — showing predicted positions only.`}
      </span>
    </motion.div>
  )
}
