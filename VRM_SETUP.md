# VRM Avatar Integration - NEXUS AI Assistant

## Overview
The NEXUS AI assistant now uses an **AvatarSample.vrm** (VRM - Virtual Runtime Model) avatar instead of a static tiger model. The VRM format provides real-time facial animations and expressions.

## Features Implemented

### ✅ **VRM Model Loading**
- **File**: `static/model/AvatarSample.vrm`
- **Loader**: Three.js GLTFLoader + THREE-VRM library
- **Display**: Face and upper body (head + torso)
- **Scaling**: Auto-scales to fit in viewport

### ✅ **Eye Animations**
- **Blink Detection**: Natural blink pattern using sine wave (~0.6 Hz frequency)
- **Expressions Used**:
  - `eyeBlinkLeft` - Left eye closing
  - `eyeBlinkRight` - Right eye closing
- **Synchronized**: Automatic ~4-5 second blink cycle

### ✅ **Lip & Mouth Animations**
- **Speaking Detection**: Synchronized with AI response speech
- **Expressions Used**:
  - `mouthOpen` - Mouth opening (0-1 range)
  - `mouthSmile` - Smiling/lip curl (0-1 range)
- **Animation**: Sinusoidal oscillation at 5.5 Hz while speaking
- **Smooth Fade**: Gradually closes mouth when not speaking

### ✅ **Head Movements**
- **Natural Bobbing**: Gentle sine wave oscillations at multiple frequencies
- **Mouse Tracking**: Head follows cursor position slightly
- **Speaking Pulse**: Slight scale increase when AI is speaking
- **Breathing Effect**: Continuous subtle breathing animation

### ✅ **Lighting & Glow Effects**
- **Holographic Look**: Maintained cinematic lighting setup
- **Glow Sphere**: Aura effect around avatar
- **Mood Lighting**: Lights respond to AI mood state
- **Particle System**: 760 animated particles orbiting avatar

## Technical Details

### Script Dependencies
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128/examples/js/loaders/GLTFLoader.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three-vrm@0.6/lib/three-vrm.js"></script>
```

### Key Variables (nexus-ai.html)
```javascript
let vrmModel = null;           // VRM scene object
let vrmRuntime = null;         // VRM runtime (for expressions)
let vrmBaseScale = 1;          // Base scale factor
const vrmAnimState = {         // Animation state tracking
  eyeBlinkLeft: 0,
  eyeBlinkRight: 0,
  mouthOpen: 0,
  mouthSmile: 0
};
```

### Animation Loop (30ms per frame)
1. **Blink Cycle**: 0.6 Hz sine wave, 8% of cycle for closing
2. **Mouth Animation**: 5.5 Hz sine wave while `state.isSpeaking` is true
3. **Head Rotation**: 0.25 Hz X-axis, 0.3 Hz Z-axis + mouse tracking
4. **Scale Breathing**: 1.5 Hz subtle scale pulsing
5. **VRM Update**: Called every frame with 16ms delta time

## File Structure
```
e:\PY AI\
├── nexus_server.py          (Backend server)
├── nexus-ai.html            (Updated with VRM support)
├── requirements.txt
├── VRM_SETUP.md             (This file)
└── static/
    └── model/
        └── AvatarSample.vrm (VRM Avatar model)
```

## Testing

### Local Testing
```bash
cd e:\PY AI
python nexus_server.py
# Open browser: http://localhost:5000
```

### What to Expect
- ✨ Avatar appears in center of screen
- 👀 Eyes blink naturally every 4-5 seconds
- 💬 Mouth opens/closes when AI is speaking
- 🎯 Head follows mouse movement
- 🔵 Holographic rings and particles animate around avatar
- 🎨 Colors change based on AI mood (thinking, happy, excited, etc.)

## Customization Options

### Adjust Blink Frequency
In animation loop, change `blinkTimer * 0.6`:
```javascript
const blinkPattern = Math.sin(blinkTimer * 0.6) * 0.5 + 0.5; // 0.6 = frequency
```

### Adjust Mouth Opening Amount
```javascript
vrmAnimState.mouthOpen = mouthAmount * 0.85;  // 0.85 = max open (0-1)
vrmAnimState.mouthSmile = mouthAmount * 0.5;  // 0.5 = smile intensity
```

### Adjust Animation Speed
Change `t += 0.0095` (higher = faster):
```javascript
t += 0.0095;  // Lower values = slower animations
```

### Adjust Head Rotation Sensitivity
```javascript
vrmModel.rotation.y = Math.sin(t * 0.25) * 0.04 + hoverX * 0.3;  // 0.3 = sensitivity
```

## Troubleshooting

### Avatar not appearing
- Check browser console for VRM loader errors
- Verify `AvatarSample.vrm` exists in `static/model/`
- Ensure all script tags are loading (check Network tab)

### Animations not working
- Check if `state.isSpeaking` is being set correctly
- Verify VRM has required morph targets: `eyeBlinkLeft`, `eyeBlinkRight`, `mouthOpen`, `mouthSmile`
- Try testing with a different VRM model

### Performance issues
- Reduce particle count (line with `particleCount = 760`)
- Lower animation quality settings in Three.js

## Resources
- **VRM Format**: https://vrm.dev/
- **Three-VRM Library**: https://github.com/pixiv/three-vrm
- **AvatarSample.vrm**: Sample VRM model (freely available)

---

**Status**: ✅ Fully Implemented and Tested  
**Last Updated**: 2026-05-29
