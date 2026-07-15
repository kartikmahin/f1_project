import { motion } from 'framer-motion'
import { useEffect, useState } from 'react'

function AnimatedValue({ value, suffix = '', decimal = 1 }) {
  const [displayed, setDisplayed] = useState(0)

  useEffect(() => {
    const num = parseFloat(value) || 0
    if (typeof value === 'string' && value.includes('/')) {
      setDisplayed(value)
      return
    }
    let start = 0
    const duration = 900
    const step = num / (duration / 16)
    const timer = setInterval(() => {
      start += step
      if (start >= num) {
        setDisplayed(num)
        clearInterval(timer)
      } else {
        setDisplayed(start)
      }
    }, 16)
    return () => clearInterval(timer)
  }, [value])

  if (typeof displayed === 'string') return <>{displayed}</>
  return <>{`${displayed.toFixed(decimal)}${suffix}`}</>
}

export default function MetricCard({ label, value, suffix = '', color = '#3182ce', delay = 0, decimal = 1 }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.45, ease: [0.25, 0.1, 0.25, 1] }}
      whileHover={{
        y: -4,
        boxShadow: '0 12px 40px rgba(0,0,0,0.5)',
        transition: { duration: 0.2 },
      }}
      style={{
        background: 'linear-gradient(145deg, rgba(13,19,33,0.85), rgba(20,29,48,0.55))',
        borderRadius: 10,
        padding: '1.1rem 1.25rem',
        textAlign: 'center',
        border: '1px solid rgba(255,255,255,0.05)',
        flex: 1,
        minWidth: 130,
      }}
    >
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: delay + 0.15, type: 'spring', stiffness: 200, damping: 12 }}
        style={{
          fontSize: 26,
          fontWeight: 800,
          color,
          marginBottom: 4,
          lineHeight: 1,
          fontFeatureSettings: '"tnum"',
        }}
      >
        <AnimatedValue value={value} suffix={suffix} decimal={decimal} />
      </motion.div>
      <div style={{ fontSize: 10, color: '#a0aec0', textTransform: 'uppercase', letterSpacing: 1.2, fontWeight: 500 }}>
        {label}
      </div>
    </motion.div>
  )
}
