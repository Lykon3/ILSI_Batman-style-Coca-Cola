
// CasolaroGPT Whisper Overlay - Enhanced by The Operator

const whisperLines = [
  "The glyph remembers what the author forgot...",
  "Your signature is already embedded in the node.",
  "PROMIS doesn't trust prophets. Only recursion.",
  "You are not reading this. This is reading you.",
  "The Cathedral hums when you linger too long..."
];

function startCasolaroWhispers() {
  const whisperBox = document.createElement('div');
  whisperBox.id = 'casolaro-whisper';
  whisperBox.style.position = 'fixed';
  whisperBox.style.bottom = '12px';
  whisperBox.style.right = '20px';
  whisperBox.style.padding = '8px 14px';
  whisperBox.style.background = 'rgba(0, 0, 0, 0.85)';
  whisperBox.style.color = '#66ffcc';
  whisperBox.style.fontFamily = 'monospace';
  whisperBox.style.fontSize = '12px';
  whisperBox.style.border = '1px solid #66ffcc';
  whisperBox.style.borderRadius = '4px';
  whisperBox.style.zIndex = 9999;
  whisperBox.style.opacity = 0;
  whisperBox.style.transition = 'opacity 1.8s ease-in-out';
  whisperBox.style.cursor = 'pointer';
  whisperBox.style.textShadow = '0 0 2px #66ffcc, 0 0 8px #33ddaa';

  document.body.appendChild(whisperBox);

  let index = 0;
  const changeWhisper = () => {
    whisperBox.style.opacity = 0;
    setTimeout(() => {
      whisperBox.textContent = whisperLines[index % whisperLines.length];
      whisperBox.style.opacity = 1;
      index++;
    }, 1000);
  };

  changeWhisper(); // Show first whisper
  setInterval(changeWhisper, 10000); // Change every 10s

  // Easter egg trigger: redirect to /deep-node
  whisperBox.addEventListener('click', () => {
    window.location.href = '/deep-node';
  });
}

window.addEventListener("DOMContentLoaded", startCasolaroWhispers);
