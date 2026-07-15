import { motion } from 'framer-motion'
import { FaHome, FaFlag, FaUser, FaCog } from 'react-icons/fa'

const navItems = [
  { key: 'home', label: 'Home', icon: FaHome },
  { key: 'predictions', label: 'Predictions', icon: FaFlag },
  { key: 'driver-analysis', label: 'Drivers', icon: FaUser },
  { key: 'training', label: 'Training', icon: FaCog },
]

export default function Navbar({ currentPage, onNavigate }) {
  return (
    <motion.nav
      initial={{ y: -80 }}
      animate={{ y: 0 }}
      transition={{ type: 'spring', stiffness: 100, damping: 24 }}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        zIndex: 100,
        background: 'rgba(7, 11, 20, 0.82)',
        backdropFilter: 'blur(20px)',
        WebkitBackdropFilter: 'blur(20px)',
        borderBottom: '1px solid rgba(255,255,255,0.05)',
        padding: '0 2rem',
        height: 60,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
      }}
    >
      <motion.button
        onClick={() => onNavigate('home')}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 10,
          background: 'none',
          border: 'none',
          cursor: 'pointer',
          padding: 0,
        }}
      >
        <div
          style={{
            width: 28,
            height: 28,
            borderRadius: 6,
            background: 'linear-gradient(135deg, #e10600, #ff4444)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: 14,
            fontWeight: 900,
            color: 'white',
            fontFamily: "'Orbitron', monospace",
          }}
        >
          F1
        </div>
        <span
          style={{
            fontFamily: "'Orbitron', monospace",
            fontWeight: 700,
            fontSize: 15,
            letterSpacing: 0.5,
            background: 'linear-gradient(90deg, #e10600, #ff4444)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          PREDICTOR
        </span>
      </motion.button>

      <nav style={{ display: 'flex', gap: 2 }} role="navigation" aria-label="Main navigation">
        {navItems.map(({ key, label, icon: Icon }) => {
          const isActive = currentPage === key
          return (
            <motion.button
              key={key}
              onClick={() => onNavigate(key)}
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.97 }}
              aria-current={isActive ? 'page' : undefined}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 7,
                padding: '7px 16px',
                borderRadius: 8,
                background: isActive
                  ? 'linear-gradient(135deg, rgba(225,6,0,0.18), rgba(225,6,0,0.06))'
                  : 'transparent',
                color: isActive ? '#ff4444' : '#a0aec0',
                border: isActive ? '1px solid rgba(225,6,0,0.2)' : '1px solid transparent',
                fontSize: 13,
                fontWeight: isActive ? 600 : 400,
                transition: 'all 200ms cubic-bezier(0.4, 0, 0.2, 1)',
                position: 'relative',
              }}
            >
              <Icon size={13} />
              <span style={{
                display: 'none',
                '@media (min-width: 640px)': { display: 'inline' },
              }}>
                {label}
              </span>
            </motion.button>
          )
        })}
      </nav>
    </motion.nav>
  )
}
