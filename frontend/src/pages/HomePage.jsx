import { motion } from 'framer-motion'
import { FaFlag, FaBrain, FaChartBar, FaRocket } from 'react-icons/fa'
import { TEAM_COLORS } from '../data/mockData'

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.08, delayChildren: 0.1 },
  },
}

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: [0.25, 0.1, 0.25, 1] },
  },
}

const features = [
  { icon: FaBrain, title: 'Neural Network Ensemble', desc: 'Multiple deep learning models working together for robust predictions with confidence estimation.' },
  { icon: FaChartBar, title: 'Uncertainty Estimation', desc: 'Every prediction includes a confidence score and uncertainty range for informed decision-making.' },
  { icon: FaFlag, title: 'Any Grand Prix', desc: 'Select any race from 2024-2026 — past or future — and get instant predictions.' },
  { icon: FaRocket, title: 'Real-time Analysis', desc: 'Side-by-side comparisons for past races with accuracy metrics and driver deep dives.' },
]

const teamEntries = Object.entries(TEAM_COLORS)

export default function HomePage({ onGetStarted }) {
  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      style={{ paddingTop: 80, position: 'relative', zIndex: 1 }}
    >
      <motion.div
        variants={itemVariants}
        style={{
          textAlign: 'center',
          padding: '3.5rem 2rem 2.5rem',
          maxWidth: 720,
          margin: '0 auto',
        }}
      >
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', stiffness: 120, damping: 14, delay: 0.15 }}
          style={{
            width: 72,
            height: 72,
            borderRadius: 18,
            background: 'linear-gradient(135deg, rgba(225,6,0,0.15), rgba(225,6,0,0.05))',
            border: '1px solid rgba(225,6,0,0.15)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: 32,
            margin: '0 auto 20px',
          }}
        >
          <span style={{ filter: 'grayscale(0.2)' }}>🏎️</span>
        </motion.div>

        <motion.h1
          variants={itemVariants}
          style={{
            fontFamily: "'Orbitron', monospace",
            fontSize: 42,
            fontWeight: 900,
            background: 'linear-gradient(90deg, #e10600, #ff4444, #ff6b6b, #ff4444, #e10600)',
            backgroundSize: '200% auto',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            animation: 'shimmer 4s linear infinite',
            marginBottom: 12,
            lineHeight: 1.15,
            letterSpacing: -0.5,
          }}
        >
          F1 Race Predictor
        </motion.h1>

        <motion.p
          variants={itemVariants}
          style={{
            color: '#a0aec0',
            fontSize: 16,
            lineHeight: 1.7,
            marginBottom: 28,
            maxWidth: 540,
            margin: '0 auto 28px',
          }}
        >
          State-of-the-art race result prediction engine powered by neural network ensembles.
          Predict any Grand Prix with confidence.
        </motion.p>

        <motion.button
          variants={itemVariants}
          whileHover={{ scale: 1.04, boxShadow: '0 0 40px rgba(225,6,0,0.3)' }}
          whileTap={{ scale: 0.97 }}
          onClick={onGetStarted}
          style={{
            background: 'linear-gradient(135deg, #e10600, #ff3333)',
            color: 'white',
            padding: '14px 36px',
            borderRadius: 10,
            fontSize: 15,
            fontWeight: 700,
            border: 'none',
            cursor: 'pointer',
            boxShadow: '0 4px 20px rgba(225,6,0,0.25)',
            display: 'inline-flex',
            alignItems: 'center',
            gap: 10,
            letterSpacing: 0.3,
          }}
        >
          <FaRocket size={14} />
          Get Started
        </motion.button>
      </motion.div>

      <motion.div
        variants={itemVariants}
        style={{
          display: 'flex',
          gap: 0,
          height: 3,
          maxWidth: 800,
          margin: '0 auto 2.5rem',
          borderRadius: 2,
          overflow: 'hidden',
          opacity: 0.6,
        }}
      >
        {teamEntries.map(([name, color]) => (
          <div key={name} title={name} style={{ flex: 1, background: color }} />
        ))}
      </motion.div>

      <motion.div
        variants={containerVariants}
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
          gap: 18,
          maxWidth: 1040,
          margin: '0 auto',
          padding: '0 2rem 3.5rem',
        }}
      >
        {features.map(({ icon: Icon, title, desc }, i) => (
          <motion.div
            key={title}
            variants={itemVariants}
            whileHover={{
              y: -6,
              boxShadow: '0 12px 40px rgba(0,0,0,0.5)',
              transition: { duration: 0.2 },
            }}
            style={{
              background: 'linear-gradient(145deg, rgba(13,19,33,0.85), rgba(20,29,48,0.55))',
              borderRadius: 14,
              padding: '1.75rem',
              border: '1px solid rgba(255,255,255,0.04)',
              backdropFilter: 'blur(8px)',
            }}
          >
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.4 + i * 0.1, type: 'spring', stiffness: 200, damping: 14 }}
              style={{
                width: 40,
                height: 40,
                borderRadius: 10,
                background: 'linear-gradient(135deg, rgba(225,6,0,0.15), rgba(225,6,0,0.05))',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: 14,
                color: '#ff4444',
                fontSize: 17,
              }}
            >
              <Icon />
            </motion.div>
            <h3 style={{ fontSize: 16, fontWeight: 700, color: '#f7fafc', marginBottom: 6 }}>{title}</h3>
            <p style={{ color: '#a0aec0', fontSize: 13, lineHeight: 1.7 }}>{desc}</p>
          </motion.div>
        ))}
      </motion.div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1, duration: 0.5 }}
        style={{
          textAlign: 'center',
          padding: '1.5rem',
          borderTop: '1px solid rgba(255,255,255,0.04)',
          color: '#4a5568',
          fontSize: 12,
          letterSpacing: 0.5,
        }}
      >
        Neural Network Ensemble with Uncertainty Estimation
      </motion.div>
    </motion.div>
  )
}
