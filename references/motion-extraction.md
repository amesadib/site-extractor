# Motion & graphics extraction

## 1. Pure CSS motion
Grep every stylesheet:
```
grep -rniE '@keyframes|animation|transition|transform|will-change|@media \(prefers-reduced-motion' cssdir
```
Capture per animation: name, duration, timing-function (easing), delay, iteration,
and the `@keyframes` body. Easing + duration are what make motion feel identical.

## 2. Detect JS motion libraries (from network assets)
| Signal in asset URLs / globals | Library | How to port |
|---|---|---|
| `gsap`, `TweenMax` | GSAP | reinstall `gsap`, copy tween config, easing, stagger |
| `ScrollTrigger` | GSAP ScrollTrigger | copy trigger, start/end, scrub, pin |
| `lottie`, `bodymovin`, `*.json` with `"v","fr","layers"` | Lottie | download JSON, render with `lottie-web`/`@lottiefiles` |
| `framer`, `data-framer-name` | Framer / Framer Motion | rebuild with `framer-motion` variants |
| `three`, `.glb`, `.hdr` | Three.js / WebGL | copy scene setup + shaders |
| `lenis`, `locomotive` | Smooth scroll | reinstall Lenis, match lerp/duration |
| `swiper` | Swiper | copy slide config |
| `rive`, `.riv` | Rive | download .riv, render with rive-js |

## 3. Lottie (most portable)
The `.json` bodymovin file is self-contained. Download it and render:
```html
<lottie-player src="anim.json" autoplay loop></lottie-player>
```

## 4. Scroll / reveal effects
Note IntersectionObserver reveals, parallax, sticky/pin sections, and scrub-linked
timelines. Reproduce with the same trigger points and easing.

## 5. Accessibility
Always carry over (or add) a `prefers-reduced-motion` fallback.
