const maxApi = require("max-api");
const { spawn } = require("node:child_process");
const fs = require("node:fs");

const DEBOUNCE_MS = 300;
const SAY_PATH = "/usr/bin/say";
const SAY_CMD = fs.existsSync(SAY_PATH) ? SAY_PATH : "say";

let lastSpokenAt = 0;
let activeProcess = null;
let activeLabel = "";

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

function clearActiveProcess(proc) {
  if (activeProcess !== proc) {
    return;
  }

  activeProcess = null;
  activeLabel = "";
}

function stopActiveProcess(reason) {
  const proc = activeProcess;
  if (!proc) {
    return false;
  }

  if (reason) {
    maxApi.post(`[ClipAnnouncer:TTS] stopping speech: ${reason}`);
  }

  try {
    proc.kill("SIGTERM");
  } catch (err) {
    maxApi.post(`[ClipAnnouncer:TTS][ERROR] ${err.message}`);
  }

  clearActiveProcess(proc);
  return true;
}

function speak(label, text) {
  const cleaned = sanitize(text);
  const cleanedLabel = sanitize(label).toUpperCase();
  let replacingActiveSpeech = false;

  if (!cleaned) {
    maxApi.post("[ClipAnnouncer:TTS] empty speech payload; skipping");
    return;
  }

  if (activeProcess) {
    if (activeLabel === cleanedLabel) {
      stopActiveProcess(`repeat ${cleanedLabel || "speech"} trigger`);
      return;
    }

    stopActiveProcess(`switching from ${activeLabel || "speech"} to ${cleanedLabel || "speech"}`);
    replacingActiveSpeech = true;
  }

  if (!replacingActiveSpeech && !canSpeakNow()) {
    return;
  }

  if (replacingActiveSpeech) {
    lastSpokenAt = Date.now();
  }

  try {
    maxApi.post(`[ClipAnnouncer:TTS] speaking: ${cleaned}`);
    const proc = spawn(SAY_CMD, [cleaned], { stdio: ["ignore", "ignore", "pipe"] });
    activeProcess = proc;
    activeLabel = cleanedLabel;

    proc.on("error", (err) => {
      maxApi.post(`[ClipAnnouncer:TTS][ERROR] ${err.message}`);
      clearActiveProcess(proc);
    });

    if (proc.stderr) {
      proc.stderr.on("data", (buf) => {
        const msg = String(buf || "").trim();
        if (msg) {
          maxApi.post(`[ClipAnnouncer:TTS][stderr] ${msg}`);
        }
      });
    }

    proc.on("exit", (code, signal) => {
      if (code !== 0 && signal !== "SIGTERM") {
        maxApi.post(`[ClipAnnouncer:TTS][ERROR] say exited code=${code} signal=${signal || "none"}`);
      }
      clearActiveProcess(proc);
    });
  } catch (err) {
    maxApi.post(`[ClipAnnouncer:TTS][ERROR] ${err.message}`);
    activeProcess = null;
    activeLabel = "";
  }
}

maxApi.addHandler("announce", (label, ...parts) => {
  speak(label, parts.join(" "));
});

maxApi.addHandler("speak", (...parts) => {
  speak("", parts.join(" "));
});

maxApi.addHandler("speak_test", () => {
  speak("", "Clip announcer speech test");
});

maxApi.addHandler("stop", () => {
  stopActiveProcess("external stop");
});

maxApi.post(`[ClipAnnouncer:TTS] ready (cmd=${SAY_CMD})`);
