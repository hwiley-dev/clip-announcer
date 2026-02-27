autowatch = 1;
inlets = 1;
outlets = 1;

var REFRESH_DELAY_MS = 25;
var ANNOUNCE_DEBOUNCE_MS = 300;

var liveSetApi = null;
var viewApi = null;

var refreshTask = null;
var announceCooldownUntil = 0;
var state = null;
var lastStateSignature = "";

function loadbang() {
    // In M4L, wait for live.thisdevice before binding LiveAPI objects.
}

function init() {
    try {
        refreshTask = new Task(refreshState, this);

        liveSetApi = new LiveAPI("live_set");
        viewApi = new LiveAPI(onViewChanged, "live_set view");

        if (!isApiObject(viewApi)) {
            postError("Unable to bind to live_set view.");
            return;
        }

        // Avoid non-listenable properties to keep console clean.
        viewApi.property = "selected_track";
        viewApi.property = "selected_scene";

        postInfo("init complete");
        refreshState();
    } catch (e) {
        postError("init failed: " + e);
    }
}

function onViewChanged() {
    if (!refreshTask) {
        return;
    }

    refreshTask.cancel();
    refreshTask.schedule(REFRESH_DELAY_MS);
}

function bang() {
    announce();
}

function msg_int(v) {
    if (v > 0) {
        announce();
    }
}

function msg_float(v) {
    if (v > 0) {
        announce();
    }
}

function list() {
    var args = arrayfromargs(arguments);
    if (args.length === 0) {
        return;
    }

    var first = parseFloat(args[0]);
    if (!isNaN(first) && first > 0) {
        announce();
    }
}

function announce() {
    performAnnounce("ANNOUNCE", buildSummary);
}

function announce_where() {
    performAnnounce("WHERE", buildWhereSummary);
}

function announce_what() {
    performAnnounce("WHAT", buildWhatSummary);
}

function announce_state() {
    performAnnounce("STATE", buildStateSummary);
}

function performAnnounce(label, buildFn) {
    var now = Date.now();
    if (now < announceCooldownUntil) {
        postInfo("announce skipped (debounce)");
        return;
    }

    announceCooldownUntil = now + ANNOUNCE_DEBOUNCE_MS;

    refreshState();
    if (!state) {
        postError("announce aborted: state unavailable");
        return;
    }

    var summary = buildFn(state);
    postInfo(label + " -> " + summary);
    outlet(0, "speak", summary);
}

function refresh() {
    refreshState();
}

function dump_state() {
    refreshState();
    postInfo(JSON.stringify(state));
}

function refreshState() {
    try {
        if (!viewApi || !isApiObject(viewApi)) {
            init();
            return;
        }

        var next = buildStateSnapshot();
        state = next;

        var sig = makeSignature(next);
        if (sig !== lastStateSignature) {
            lastStateSignature = sig;
            postStructured(next);
        }
    } catch (e) {
        postError("refreshState failed: " + e);
    }
}

function buildStateSnapshot() {
    var next = {
        track_index: -1,
        track_name: "Unknown Track",
        track_id: 0,
        slot_index: -1,
        slot_id: 0,
        has_clip: 0,
        clip_id: 0,
        clip_name: "Empty",
        clip_length: 0,
        looping: 0,
        loop_start: 0,
        loop_end: 0,
        status: "Stopped"
    };

    var trackId = parseId(safeGet(viewApi, "selected_track"));
    next.track_id = trackId;

    if (trackId > 0) {
        var trackApi = safeApiFromId(trackId);
        next.track_index = findTrackIndex(trackId);
        if (hasObjectId(trackApi)) {
            next.track_name = safeGetString(trackApi, "name", "Unknown Track");
            if (next.track_index < 1) {
                var trackIndexFromPath = parseTrackIndex(getApiPath(trackApi));
                if (trackIndexFromPath >= 0) {
                    next.track_index = trackIndexFromPath + 1;
                }
            }
        }
    }

    var selectedSceneId = parseId(safeGet(viewApi, "selected_scene"));
    var selectedSceneIndex = findSceneIndex(selectedSceneId);
    if (selectedSceneIndex >= 0) {
        next.slot_index = selectedSceneIndex;
    }

    var slotId = parseId(safeGet(viewApi, "highlighted_clip_slot"));
    next.slot_id = slotId;

    var slotApi = null;
    if (next.track_index > 0 && selectedSceneIndex >= 0) {
        slotApi = safeApiFromPath("live_set tracks " + (next.track_index - 1) + " clip_slots " + selectedSceneIndex);
        if (hasObjectId(slotApi)) {
            next.slot_id = parseId(slotApi.id);
        }
    }

    if (!hasObjectId(slotApi) && slotId > 0) {
        slotApi = safeApiFromId(slotId);
    }

    if (!hasObjectId(slotApi)) {
        return next;
    }

    var slotPath = getApiPath(slotApi);
    var slotIndexFromPath = parseClipSlotIndex(slotPath);
    if (slotIndexFromPath >= 0) {
        next.slot_index = slotIndexFromPath;
    } else if (next.track_index > 0) {
        next.slot_index = findSlotIndex(next.track_index - 1, next.slot_id);
    } else {
        // Keep slot index from selected_scene fallback if available.
    }

    next.has_clip = safeGetInt(slotApi, "has_clip", 0);

    var isRecording = safeGetInt(slotApi, "is_recording", 0);
    var isPlaying = safeGetInt(slotApi, "is_playing", 0);
    if (isRecording === 1) {
        next.status = "Recording";
    } else if (isPlaying === 1) {
        next.status = "Playing";
    } else {
        next.status = "Stopped";
    }

    if (next.has_clip !== 1) {
        return next;
    }

    var clipId = parseId(safeGet(slotApi, "clip"));
    next.clip_id = clipId;

    var clipApi = safeApiFromId(clipId);
    if (!hasObjectId(clipApi)) {
        return next;
    }

    next.clip_name = safeGetString(clipApi, "name", "(Unnamed Clip)");
    next.clip_length = safeGetFloat(clipApi, "length", 0);
    next.looping = safeGetInt(clipApi, "looping", 0);
    next.loop_start = safeGetFloat(clipApi, "loop_start", 0);
    next.loop_end = safeGetFloat(clipApi, "loop_end", next.clip_length);

    return next;
}

function makeSignature(s) {
    return [
        s.track_id,
        s.slot_id,
        s.has_clip,
        s.clip_id,
        s.status,
        s.looping,
        s.loop_start,
        s.loop_end
    ].join("|");
}

function buildSummary(s) {
    return [buildWhereSummary(s), buildWhatSummary(s), buildStateSummary(s)].join(" ");
}

function buildWhereSummary(s) {
    var trackIndexText = s.track_index > 0 ? s.track_index : "?";
    var slotIndexText = s.slot_index >= 0 ? (s.slot_index + 1) : "?";
    var trackName = safeLabel(s.track_name, "Unknown Track");

    return "Track " + trackIndexText + ": " + trackName + ". Slot " + slotIndexText + ".";
}

function buildWhatSummary(s) {
    var clipName = s.has_clip === 1 ? safeLabel(s.clip_name, "(Unnamed Clip)") : "Empty";
    if (s.has_clip !== 1) {
        return "Clip: " + clipName + ".";
    }

    var lengthText = formatBeats(s.clip_length);
    var loopStartText = formatBeats(s.loop_start);
    var loopEndText = formatBeats(s.loop_end);
    var loopingText = s.looping === 1 ? "On" : "Off";

    return "Clip: " + clipName + ". Length: " + lengthText + " beats. Loop: " + loopingText + ", " + loopStartText + " to " + loopEndText + " beats.";
}

function buildStateSummary(s) {
    return "Status: " + s.status + ".";
}

function formatBeats(n) {
    var value = parseFloat(n);
    if (isNaN(value)) {
        return "0";
    }

    var rounded = Math.round(value * 100) / 100;
    if (Math.abs(rounded - Math.round(rounded)) < 0.0001) {
        return String(Math.round(rounded));
    }

    return String(rounded);
}

function postStructured(s) {
    postInfo("STATE " + JSON.stringify(s));
    postInfo("SUMMARY " + buildSummary(s));
}

function postInfo(msg) {
    post("[ClipAnnouncer] " + msg + "\n");
}

function postError(msg) {
    post("[ClipAnnouncer][ERROR] " + msg + "\n");
}

function safeApiFromId(id) {
    try {
        if (!id || id <= 0) {
            return null;
        }
        return new LiveAPI("id " + id);
    } catch (e) {
        postError("safeApiFromId(" + id + ") failed: " + e);
        return null;
    }
}

function safeApiFromPath(pathText) {
    try {
        if (!pathText) {
            return null;
        }
        return new LiveAPI(pathText);
    } catch (e) {
        postError("safeApiFromPath(" + pathText + ") failed: " + e);
        return null;
    }
}

function isApiObject(api) {
    try {
        return api !== null && api !== undefined;
    } catch (e) {
        return false;
    }
}

function hasObjectId(api) {
    try {
        return isApiObject(api) && api.id > 0;
    } catch (e) {
        return false;
    }
}

function getApiPath(api) {
    try {
        if (!isApiObject(api)) {
            return "";
        }

        if (api.unquotedpath) {
            return String(api.unquotedpath);
        }

        if (api.path) {
            return String(api.path);
        }
    } catch (e) {
        postError("getApiPath failed: " + e);
    }

    return "";
}

function safeGet(api, prop) {
    try {
        if (!isApiObject(api)) {
            return null;
        }
        return api.get(prop);
    } catch (e) {
        postError("get " + prop + " failed: " + e);
        return null;
    }
}

function safeGetString(api, prop, fallback) {
    var raw = safeGet(api, prop);
    if (raw === null || raw === undefined) {
        return fallback;
    }

    if (raw.constructor === Array) {
        if (raw.length === 0) {
            return fallback;
        }
        if (raw[0] === "id") {
            return fallback;
        }
        return String(raw.join(" "));
    }

    var s = String(raw);
    return s.length > 0 ? s : fallback;
}

function safeGetInt(api, prop, fallback) {
    var raw = safeGet(api, prop);
    var n = parseNumber(raw);
    if (isNaN(n)) {
        return fallback;
    }
    return parseInt(n, 10);
}

function safeGetFloat(api, prop, fallback) {
    var raw = safeGet(api, prop);
    var n = parseNumber(raw);
    if (isNaN(n)) {
        return fallback;
    }
    return n;
}

function parseNumber(raw) {
    if (raw === null || raw === undefined) {
        return NaN;
    }

    if (raw.constructor === Array) {
        if (raw.length === 0) {
            return NaN;
        }
        if (raw[0] === "id") {
            return parseFloat(raw[1]);
        }
        return parseFloat(raw[0]);
    }

    return parseFloat(raw);
}

function parseId(raw) {
    if (raw === null || raw === undefined) {
        return 0;
    }

    if (raw.constructor === Array) {
        if (raw.length >= 2 && raw[0] === "id") {
            return parseInt(raw[1], 10) || 0;
        }
        if (raw.length >= 1) {
            return parseInt(raw[0], 10) || 0;
        }
        return 0;
    }

    var text = String(raw);
    if (text.indexOf("id") === 0) {
        var bits = text.split(" ");
        if (bits.length > 1) {
            return parseInt(bits[1], 10) || 0;
        }
    }

    return parseInt(text, 10) || 0;
}

function parseClipSlotIndex(pathText) {
    if (!pathText) {
        return -1;
    }

    var m = String(pathText).match(/clip_slots\s+(\d+)/);
    if (!m || m.length < 2) {
        return -1;
    }

    return parseInt(m[1], 10);
}

function parseTrackIndex(pathText) {
    if (!pathText) {
        return -1;
    }

    var m = String(pathText).match(/tracks\s+(\d+)/);
    if (!m || m.length < 2) {
        return -1;
    }

    return parseInt(m[1], 10);
}

function findTrackIndex(targetTrackId) {
    try {
        if (!isApiObject(liveSetApi)) {
            return -1;
        }

        var count = liveSetApi.getcount("tracks");
        var i;
        for (i = 0; i < count; i++) {
            var t = new LiveAPI("live_set tracks " + i);
            if (hasObjectId(t) && idsEqual(t.id, targetTrackId)) {
                return i + 1;
            }
        }
    } catch (e) {
        postError("findTrackIndex failed: " + e);
    }

    return -1;
}

function findSlotIndex(trackIndexZeroBased, targetSlotId) {
    try {
        var trackApi = new LiveAPI("live_set tracks " + trackIndexZeroBased);
        if (!hasObjectId(trackApi)) {
            return -1;
        }

        var count = trackApi.getcount("clip_slots");
        var i;
        for (i = 0; i < count; i++) {
            var slotApi = new LiveAPI("live_set tracks " + trackIndexZeroBased + " clip_slots " + i);
            if (hasObjectId(slotApi) && idsEqual(slotApi.id, targetSlotId)) {
                return i;
            }
        }
    } catch (e) {
        postError("findSlotIndex failed: " + e);
    }

    return -1;
}

function findSceneIndex(targetSceneId) {
    try {
        if (!isApiObject(liveSetApi) || !targetSceneId || targetSceneId <= 0) {
            return -1;
        }

        var count = liveSetApi.getcount("scenes");
        var i;
        for (i = 0; i < count; i++) {
            var sceneApi = new LiveAPI("live_set scenes " + i);
            if (hasObjectId(sceneApi) && idsEqual(sceneApi.id, targetSceneId)) {
                return i;
            }
        }
    } catch (e) {
        postError("findSceneIndex failed: " + e);
    }

    return -1;
}

function safeLabel(text, fallback) {
    if (text === null || text === undefined) {
        return fallback;
    }

    var s = String(text).replace(/[\r\n\t]+/g, " ").replace(/\s+/g, " ").trim();
    return s.length > 0 ? s : fallback;
}

function idsEqual(a, b) {
    return parseId(a) === parseId(b);
}
