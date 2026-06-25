/* =========================================================
   TERNAH — scroll-driven glossy 3D logo hero
   Built from the exact brand-mark SVG path data (viewBox 0 0 100 94).
   ========================================================= */
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const section = document.getElementById('hero3d');
const canvasEl = document.getElementById('logo3d');

function hasWebGL() {
  try {
    const c = document.createElement('canvas');
    return !!(window.WebGLRenderingContext && (c.getContext('webgl') || c.getContext('experimental-webgl')));
  } catch (e) { return false; }
}

if (section && canvasEl && hasWebGL()) {
  init();
}
// else: the static CSS fallback in the markup stays visible

function buildLogoShapes() {
  const s = 0.046;          // scale from SVG units to 3D units
  const cx = 50, cy = 47;   // visual center of the 100x94 viewBox
  const pt = (x, y) => [(x - cx) * s, -(y - cy) * s];

  const shape1 = new THREE.Shape();
  shape1.moveTo(...pt(27, 14));
  shape1.lineTo(...pt(45, 14));
  shape1.bezierCurveTo(...pt(47, 14), ...pt(48, 16), ...pt(47, 18));
  shape1.lineTo(...pt(38, 41));
  shape1.bezierCurveTo(...pt(37, 43), ...pt(34, 43), ...pt(33, 41));
  shape1.lineTo(...pt(24, 19));
  shape1.bezierCurveTo(...pt(23, 16), ...pt(24, 14), ...pt(27, 14));

  const shape2 = new THREE.Shape();
  shape2.moveTo(...pt(58, 14));
  shape2.lineTo(...pt(84, 14));
  shape2.bezierCurveTo(...pt(86, 14), ...pt(87, 16), ...pt(87, 18));
  shape2.lineTo(...pt(87, 34));
  shape2.bezierCurveTo(...pt(87, 37), ...pt(84, 38), ...pt(82, 36));
  shape2.lineTo(...pt(74, 30));
  shape2.lineTo(...pt(34, 78));
  shape2.bezierCurveTo(...pt(33, 79), ...pt(31, 80), ...pt(29, 80));
  shape2.lineTo(...pt(18, 80));
  shape2.bezierCurveTo(...pt(15, 80), ...pt(14, 77), ...pt(16, 75));
  shape2.lineTo(...pt(58, 14));

  const shape3 = new THREE.Shape();
  shape3.moveTo(...pt(73, 78));
  shape3.lineTo(...pt(55, 78));
  shape3.bezierCurveTo(...pt(53, 78), ...pt(52, 76), ...pt(53, 74));
  shape3.lineTo(...pt(62, 51));
  shape3.bezierCurveTo(...pt(63, 49), ...pt(66, 49), ...pt(67, 51));
  shape3.lineTo(...pt(76, 73));
  shape3.bezierCurveTo(...pt(77, 76), ...pt(76, 78), ...pt(73, 78));

  return [shape1, shape2, shape3];
}

function buildLogoGroup() {
  const extrudeSettings = {
    depth: 0.5, bevelEnabled: true, bevelThickness: 0.045,
    bevelSize: 0.045, bevelSegments: 8, curveSegments: 28,
  };
  const material = new THREE.MeshPhysicalMaterial({
    color: 0x2f4cff,
    metalness: 0.3,
    roughness: 0.06,
    clearcoat: 1,
    clearcoatRoughness: 0.05,
    reflectivity: 1,
    envMapIntensity: 1.6,
  });

  const group = new THREE.Group();
  buildLogoShapes().forEach((shape) => {
    const geo = new THREE.ExtrudeGeometry(shape, extrudeSettings);
    group.add(new THREE.Mesh(geo, material));
  });
  return group;
}

function init() {
  const canvas = canvasEl;
  const fallback = document.querySelector('.hero3d-fallback');
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  } catch (e) {
    return; // keep static fallback
  }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.1;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 100);
  camera.position.set(0, 0, 7.2);

  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;

  const key = new THREE.DirectionalLight(0xffffff, 1.5);
  key.position.set(3, 5, 5);
  scene.add(key);
  const rim = new THREE.DirectionalLight(0x4d68ff, 1.1);
  rim.position.set(-4, -2, -4);
  scene.add(rim);
  scene.add(new THREE.AmbientLight(0xffffff, 0.25));

  const logo = buildLogoGroup();
  logo.rotation.x = 0.18;
  scene.add(logo);

  function resize() {
    const w = canvas.clientWidth || 1, h = canvas.clientHeight || 1;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  window.addEventListener('resize', resize);
  resize();

  const panels = document.querySelectorAll('.h3p');
  const dots = document.querySelectorAll('.hero3d-dots span');
  const scrollHint = document.querySelector('.hero3d-scrollhint');
  let progress = 0;

  function updateProgress() {
    const rect = section.getBoundingClientRect();
    const total = section.offsetHeight - window.innerHeight;
    const scrolled = -rect.top;
    progress = Math.min(Math.max(total > 0 ? scrolled / total : 0, 0), 1);
    updatePanels();
  }

  function updatePanels() {
    const n = panels.length;
    panels.forEach((p, i) => {
      const center = (i + 0.5) / n;
      const dist = Math.abs(progress - center);
      const range = (1 / n) * 0.62;
      let op = 1 - Math.min(dist / range, 1);
      op = Math.max(op, 0);
      p.style.opacity = op;
      p.style.transform = `translateY(${(progress - center) * 50}px)`;
      p.style.pointerEvents = op > 0.5 ? 'auto' : 'none';
    });
    dots.forEach((d, i) => d.classList.toggle('active', i === Math.min(Math.floor(progress * n), n - 1)));
    if (scrollHint) scrollHint.style.opacity = progress > 0.05 ? '0' : '1';
  }

  window.addEventListener('scroll', updateProgress, { passive: true });
  updateProgress();

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let autoT = 0;
  let firstFrame = true;

  function animate() {
    if (!reduceMotion) autoT += 0.0032;
    logo.rotation.y = progress * Math.PI * 2.4 + autoT;
    logo.rotation.x = 0.18 + Math.sin(autoT * 0.6) * 0.05;
    logo.position.y = -progress * 0.55;
    logo.position.z = progress * 0.6;
    const scale = 1 + progress * 0.22;
    logo.scale.set(scale, scale, scale);
    renderer.render(scene, camera);
    if (firstFrame) {
      canvas.classList.add('ready');
      if (fallback) fallback.style.opacity = '0';
      firstFrame = false;
    }
    requestAnimationFrame(animate);
  }
  animate();
}
