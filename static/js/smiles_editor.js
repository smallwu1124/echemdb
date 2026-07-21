/**
 * Molecular Structure Editor (Singleton Modal Pattern)
 * - One global modal, never destroyed
 * - Preview images always on white background
 * - SMILES text always visible as fallback
 */

var jsmeApplet = null;
var jsmeLoaded = false;
var jsmeActiveTarget = null;
var jsmeActiveNameId = null;
var editorInitialized = false;

function jsmeOnLoad() { jsmeLoaded = true; }

function initJSME(cid, w, h) {
    if (typeof JSApplet === "undefined") return null;
    try {
        jsmeApplet = new JSApplet.JSME(cid, w, h);
        jsmeLoaded = true;
        return jsmeApplet;
    } catch(e) { return null; }
}

function getSmiles() {
    return (jsmeApplet && jsmeLoaded) ? jsmeApplet.smiles() : "";
}

function setSmiles(s) {
    if (jsmeApplet && jsmeLoaded && s)
        try { jsmeApplet.readString(s); } catch(e) {}
}

function clearEditor() {
    if (jsmeApplet && jsmeLoaded) jsmeApplet.readString("");
}

async function lookupNameFromSmiles(smiles) {
    if (!smiles) return "";
    try {
        var r = await fetch("/api/smiles/name", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({smiles: smiles})
        });
        var d = await r.json();
        return d.name || "";
    } catch(e) { return ""; }
}

function renderSmilesImg(smiles, cid) {
    var el = document.getElementById(cid);
    if (!el) return;
    el.innerHTML = "";
    var img = document.createElement("img");
    img.src = "/struct-img/" + encodeURIComponent(smiles);
    img.alt = smiles;
    img.style.cssText = "max-width:180px;max-height:120px;border-radius:4px;background:#ffffff;padding:4px;";
    el.appendChild(img);
}

function updatePreview(smiles, pid) {
    if (!smiles || !pid) return;
    var c = document.getElementById(pid);
    if (!c) return;
    c.innerHTML = "";

    // Try SmilesDrawer with white background
    if (typeof SmilesDrawer !== "undefined") {
        try {
            var cv = document.createElement("canvas");
            cv.id = pid + "_canvas";
            cv.width = 180; cv.height = 120;
            cv.style.cssText = "border:1px solid var(--border);border-radius:4px;max-width:100%;background:#ffffff;";
            c.appendChild(cv);
            var dr = new SmilesDrawer.Drawer({width: 180, height: 120});
            SmilesDrawer.parse(smiles, function(t) { dr.draw(t, cv.id, "light", false); });
            var lb = document.createElement("div");
            lb.style.cssText = "font-size:0.7rem;color:var(--text-dim);margin-top:0.25rem;font-family:monospace;word-break:break-all;";
            lb.textContent = smiles;
            c.appendChild(lb);
            return;
        } catch(e) { c.innerHTML = ""; }
    }

    // Fallback: PubChem image with white background
    renderSmilesImg(smiles, pid);
    var lb = document.createElement("div");
    lb.style.cssText = "font-size:0.7rem;color:var(--text-dim);margin-top:0.25rem;font-family:monospace;word-break:break-all;";
    lb.textContent = smiles;
    c.appendChild(lb);
}

// ---- Singleton Modal ----
// Initialize modal content once on first open
function initEditorModal() {
    if (editorInitialized) return;
    editorInitialized = true;

    var container = document.getElementById("jsme_editor_container");
    if (!container) return;
    container.innerHTML = "";

    // SMILES text input (always works)
    var textInput = document.createElement("input");
    textInput.type = "text";
    textInput.id = "smiles_text_input";
    textInput.placeholder = "Enter SMILES or draw below...";
    textInput.style.cssText = "width:100%;padding:0.5rem 0.6rem;" +
        "background:#15151b;border:1px solid #2a2a33;border-radius:4px;" +
        "color:#e4e4e7;font-family:monospace;font-size:0.85rem;outline:none;box-sizing:border-box;";
    container.appendChild(textInput);

    // Try JSME if available (loads external CDN)
    if (typeof JSApplet !== "undefined") {
        try {
            var jsmeDiv = document.createElement("div");
            jsmeDiv.id = "jsme_instance";
            jsmeDiv.style.cssText = "width:420px;height:320px;margin:10px auto;";
            container.appendChild(jsmeDiv);
            setTimeout(function() {
                initJSME("jsme_instance", "420px", "320px");
            }, 200);
        } catch(e) {}
    }

    // Save button handler (bound once)
    var saveBtn = document.getElementById("jsme_save_btn");
    if (saveBtn) {
        saveBtn.onclick = function() {
            var modal = document.getElementById("jsmeModal");
            var target = jsmeActiveTarget;
            if (!target) return;

            var smiles = "";
            if (jsmeApplet && jsmeLoaded) {
                smiles = jsmeApplet.smiles();
            } else {
                var t = document.getElementById("smiles_text_input");
                if (t) smiles = t.value.trim();
            }
            if (!smiles) { alert("Please draw or enter a SMILES structure"); return; }

            // Write to target input
            document.getElementById(target).value = smiles;

            // Look up name
            lookupNameFromSmiles(smiles).then(function(name) {
                if (name && jsmeActiveNameId && document.getElementById(jsmeActiveNameId)) {
                    document.getElementById(jsmeActiveNameId).value = name;
                }
            });

            // Update preview
            updatePreview(smiles, target + "_preview");

            // Hide modal (not destroy)
            modal.style.display = "none";
            document.body.style.overflow = "";
            jsmeActiveTarget = null;
        };
    }

    // Close button handler
    var closeBtn = document.querySelector("#jsmeModal .jsme-close");
    if (closeBtn) {
        closeBtn.onclick = function() {
            document.getElementById("jsmeModal").style.display = "none";
            document.body.style.overflow = "";
            jsmeActiveTarget = null;
        };
    }

    // Click backdrop to close
    var modal = document.getElementById("jsmeModal");
    if (modal) {
        modal.onclick = function(e) {
            if (e.target === modal) {
                modal.style.display = "none";
                document.body.style.overflow = "";
                jsmeActiveTarget = null;
            }
        };
    }
}

// Open editor modal (show, don't recreate)
function openMoleculeEditor(modalId, targetId, nameId) {
    jsmeActiveTarget = targetId;
    jsmeActiveNameId = nameId || null;

    // Initialize editor content once
    initEditorModal();

    // Load current value into text input
    var srcInput = document.getElementById(targetId);
    var currentSmiles = srcInput ? srcInput.value : "";
    var textInput = document.getElementById("smiles_text_input");
    if (textInput) {
        textInput.value = currentSmiles;
        textInput.focus();
        textInput.select();
    }

    // Load current value into JSME if available
    if (currentSmiles && jsmeApplet && jsmeLoaded) {
        try { jsmeApplet.readString(currentSmiles); } catch(e) {}
    }

    // Show modal
    var modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = "flex";
        document.body.style.overflow = "hidden";
    }
}

// Auto-render existing SMILES on page load
document.addEventListener("DOMContentLoaded", function() {
    var ids = ["reactant_smiles","product_smiles","sim_smiles",
               "smiles","substrate_smiles","product_smiles"];
    ids.forEach(function(id) {
        var inp = document.getElementById(id);
        if (inp && inp.value) {
            setTimeout(function() { updatePreview(inp.value, id + "_preview"); }, 300);
        }
    });
});
