import { useEffect, useRef } from 'react'

function Star(canvas, ctx) {
  const x = Math.random() * canvas.width
  const y = Math.random() * canvas.height
  let size = Math.random() * 1.5 + 0.3
  const opacity = Math.random() * 0.4 + 0.1
  const twinkleSpeed = Math.random() * 0.015 + 0.003
  const hue = Math.random() * 60 + 200

  return {
    update() {
      size += Math.sin(Date.now() * twinkleSpeed) * 0.002
      ctx.beginPath()
      ctx.arc(x, y, Math.max(0.15, size), 0, Math.PI * 2)
      ctx.fillStyle = `hsla(${hue}, 30%, 80%, ${opacity})`
      ctx.fill()
    },
  }
}

function SpeedLine(canvas, ctx) {
  const x = Math.random() * canvas.width
  let y = Math.random() * canvas.height
  const length = Math.random() * 40 + 15
  const speed = Math.random() * 1.5 + 0.5
  const opacity = Math.random() * 0.04 + 0.01
  const width = Math.random() * 0.5 + 0.5

  return {
    update() {
      y += speed
      if (y > canvas.height) y = -length
      ctx.beginPath()
      ctx.moveTo(x, y)
      ctx.lineTo(x, y + length)
      ctx.strokeStyle = `rgba(255, 255, 255, ${opacity})`
      ctx.lineWidth = width
      ctx.stroke()
    },
  }
}

export default function AnimatedBackground() {
  const canvasRef = useRef(null)

  useEffect(() => {
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    let animId
    let stars = []
    let speedLines = []

    function resize() {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
      stars = Array.from({ length: 80 }, () => Star(canvas, ctx))
      speedLines = Array.from({ length: 20 }, () => SpeedLine(canvas, ctx))
    }

    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      for (const s of stars) s.update()
      for (const s of speedLines) s.update()
      animId = requestAnimationFrame(animate)
    }

    resize()
    animate()
    window.addEventListener('resize', resize)
    return () => {
      cancelAnimationFrame(animId)
      window.removeEventListener('resize', resize)
    }
  }, [])

  return (
    <canvas
      ref={canvasRef}
      aria-hidden="true"
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        zIndex: 0,
        pointerEvents: 'none',
      }}
    />
  )
}
