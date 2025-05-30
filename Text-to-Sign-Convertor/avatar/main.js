// let scene, camera, renderer, clock;
// let avatar, skeleton;

// init();
// loadAvatar();

// function init() {
//   scene = new THREE.Scene();
//   scene.background = new THREE.Color(0xeeeeee);

//   camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
//   camera.position.set(0, 1.6, 3);

//   renderer = new THREE.WebGLRenderer({ canvas: document.getElementById("avatarCanvas"), antialias: true });
//   renderer.setSize(window.innerWidth, window.innerHeight);

//   clock = new THREE.Clock();

//   const light = new THREE.DirectionalLight(0xffffff, 1);
//   light.position.set(0, 5, 5);
//   scene.add(light);

//   const ambient = new THREE.AmbientLight(0xffffff, 0.5);
//   scene.add(ambient);

//   const grid = new THREE.GridHelper(10, 10);
//   scene.add(grid);

//   const axes = new THREE.AxesHelper(1);
//   scene.add(axes);

//   window.addEventListener('resize', () => {
//     camera.aspect = window.innerWidth / window.innerHeight;
//     camera.updateProjectionMatrix();
//     renderer.setSize(window.innerWidth, window.innerHeight);
//   });
// }

// function loadAvatar() {
//   const loader = new THREE.GLTFLoader();
//   loader.load(
//     'avatar/avatar.glb',  // ✅ Your folder path
//     (gltf) => {
//       avatar = gltf.scene;
//       avatar.traverse((child) => {
//         if (child.isSkinnedMesh) {
//           skeleton = child.skeleton;
//           console.log("Skeleton loaded:", skeleton);
//         }
//       });
//       scene.add(avatar);
//       console.log("Avatar loaded");
//       animate();
//     },
//     (xhr) => {
//       console.log(`Loading avatar: ${(xhr.loaded / xhr.total * 100).toFixed(2)}%`);
//     },
//     (error) => {
//       console.error('Failed to load avatar:', error);
//     }
//   );
// }

// function animate() {
//   requestAnimationFrame(animate);
//   renderer.render(scene, camera);
// }


// Import Three.js and GLTFLoader from official CDN
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';
import { GLTFLoader } from 'https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/loaders/GLTFLoader.js';

let scene, camera, renderer, avatar;

init();
loadAvatar();

function init() {
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.z = 2;

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);

  const light = new THREE.HemisphereLight(0xffffff, 0x444444);
  light.position.set(0, 1, 0);
  scene.add(light);

  animate();
}

function loadAvatar() {
  const loader = new GLTFLoader();
  loader.load('avatar.glb', function(gltf) {
    avatar = gltf.scene;
    scene.add(avatar);
  }, undefined, function(error) {
    console.error(error);
  });
}

function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}
