import { motion } from 'framer-motion'

export default function SectionTitle({ icon, title, delay = 0 }) {
  return (
    <motion.div
      initial={{ opacity: 0, x: -12 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay, duration: 0.35, ease: [0.25, 0.1, 0.25, 1] }}
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: 10,
        fontSize: 17,
        fontWeight: 700,
        color: '#f7fafc',
        margin: '1.25rem 0 0.875rem 0',
        paddingBottom: 8,
        borderBottom: '1px solid rgba(255,255,255,0.05)',
      }}
    >
      {icon && <span style={{ fontSize: 16 }}>{icon}</span>}
      {title}
    </motion.div>
  )
}
