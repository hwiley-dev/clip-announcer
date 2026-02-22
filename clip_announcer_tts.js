const maxApi = require("max-api");
const { spawn } = require("node:child_process");
const fs = require("node:fs");

const DEBOUNCE_MS = 300;
const SAY_PATH = "/usr/bin/say";
const SAY_CMD = fs.existsSync(SAY_PATH) ? SAY_PATH : "say";

let lastSpokenAt = 0;
let activeProcess = null;

function sanitize(text) {
  return String(text || "")
    .replace(/[\r\n\t]+/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 512);
}

function canSpeakNow() {
  const now = Date.now();
  if (now - lastSpokenAt < DEBOUNCE_MS) {
    maxApi.post("[ClipAnnouncer:TTS] speak skipped (debounce)");
    return false;
  }
  lastSpokenAt = now;
  return true;
}

function speak(text) {
  const cleaned = sanitize(text);

  if (!cleaned) {
    maxApi.post("[ClipAnnouncer:TTS] empty speech payload; skipping");
    return;
  }

  if (!canSpeakNow()) {
    return;
  }

  if (activeProcess) {
    maxApi.post("[ClipAnnouncer:TTS] speak skipped (already speaking)");
    return;
  }

  try {
    maxApi.post(`[ClipAnnouncer:TTS] speaking: ${cleaned}`);
    activeProcess = spawn(SAY_CMD, [cleaned], { stdio: ["ignore", "ignore", "pipe"] });

    activeProcess.on("error", (err) => {
      maxApi.post(`[ClipAnnouncer:TTS][ERROR] ${err.message}`);
      activeProcess = null;
    });

    if (activeProcess.stderr) {
      activeProcess.stderr.on("data", (buf) => {
        const msg = String(buf || "").trim();
        if (msg) {
          maxApi.post(`[ClipAnnouncer:TTS][stderr] ${msg}`);
        }
      });
    }

    activeProcess.on("exit", (code, signal) => {
      if (code !== 0) {
        maxApi.post(`[ClipAnnouncer:TTS][ERROR] say exited code=${code} signal=${signal || "none"}`);
      }
      activeProcess = null;
    });
  } catch (err) {
    maxApi.post(`[ClipAnnouncer:TTS][ERROR] ${err.message}`);
    activeProcess = null;
  }
}

maxApi.addHandler("speak", (...parts) => {
  speak(parts.join(" "));
});

maxApi.addHandler("speak_test", () => {
  speak("Clip announcer speech test");
});

maxApi.addHandler("stop", () => {
  if (activeProcess) {
    try {
      activeProcess.kill("SIGTERM");
    } catch (err) {
      maxApi.post(`[ClipAnnouncer:TTS][ERROR] ${err.message}`);
    }
    activeProcess = null;
  }
});

maxApi.post(`[ClipAnnouncer:TTS] ready (cmd=${SAY_CMD})`);
