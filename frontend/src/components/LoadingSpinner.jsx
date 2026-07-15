import { motion } from 'framer-motion'

export default function LoadingSpinner({ text = 'Loading...' }) {
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '4rem 2rem',
        gap: 20,
      }}
    >
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ repeat: Infinity, duration: 1.2, ease: 'linear' }}
        style={{
          width: 40,
          height: 40,
          border: '2.5px solid rgba(255,255,255,0.06)',
          borderTop: '2.5px solid #e10600',
          borderRadius: '50%',
        }}
      />
      <motion.p
        initial={{ opacity: 0.4 }}
        animate={{ opacity: 1 }}
        transition={{ repeat: Infinity, duration: 1.5, repeatType: 'reverse' }}
        style={{ color: '#a0aec0', fontSize: 13, fontWeight: 500, letterSpacing: 0.3 }}
      >
        {text}
      </motion.p>
    </div>
  )
}
