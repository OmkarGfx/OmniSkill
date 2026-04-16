//! Inter-process communication for agent messaging.
//!
//! Provides tmux pane detection, message paste,
//! a JSON-RPC socket listener, and a socket client for cross-session
//! agent discovery and messaging.

use crate::*;
use std::io::{Read as IoRead, Write as IoWrite};
use std::os::unix::net::UnixListener;

const IPC_MAX_MESSAGE_SIZE: usize = 4096;
const IPC_PASTE_COOLDOWN: std::time::Duration = std::time::Duration::from_secs(5);
const IPC_PROTOCOL_VERSION: u32 = 1;

// --- Pane detection ---

/// Detected tmux pane info.
pub struct DetectedPane {
    /// Unique pane ID, e.g., "%42"
    pub unique_id: String,
    /// Display pane ID, e.g., "0:0.1"
    pub display_id: String,
    /// Session name
    pub session: String,
}

/// Walk the process tree to find which tmux pane we're in.
pub fn detect_tmux_pane() -> Option<DetectedPane> {
    let output = Command::new("tmux")
        .args([
            "list-panes",
            "-a",
            "-F",
            "#{pane_pid}\t#{pane_id}\t#{session_name}:#{window_index}.#{pane_index}\t#{session_name}",
        ])
        .output()
        .ok()?;

    if !output.status.success() {
        return None;
    }

    let text = String::from_utf8_lossy(&output.stdout);
    // Map pid -> (unique_id, display_id, session)
    let mut pane_map: HashMap<String, (String, String, String)> = HashMap::new();
    for line in text.trim().lines() {
        let parts: Vec<&str> = line.split('\t').collect();
        if parts.len() == 4 {
            pane_map.insert(
                parts[0].to_string(),
                (parts[1].to_string(), parts[2].to_string(), parts[3].to_string()),
            );
        }
    }

    let mut pid = std::process::id();
    loop {
        if pid <= 1 {
            break;
        }
        if let Some((unique_id, display_id, session)) = pane_map.get(&pid.to_string()) {
            return Some(DetectedPane {
                unique_id: unique_id.clone(),
                display_id: display_id.clone(),
                session: session.clone(),
            });
        }
        // Walk up to parent
        match Command::new("ps")
            .args(["-o", "ppid=", "-p", &pid.to_string()])
            .output()
            .ok()
            .and_then(|o| {
                String::from_utf8_lossy(&o.stdout)
                    .trim()
                    .parse::<u32>()
                    .ok()
            })
        {
            Some(ppid) if ppid != pid => pid = ppid,
            _ => break,
        }
    }
    None
}

// --- Tmux paste ---

pub fn capture_pane(pane: &str) -> String {
    Command::new("tmux")
        .args(["capture-pane", "-t", pane, "-p"])
        .output()
        .map(|o| String::from_utf8_lossy(&o.stdout).to_string())
        .unwrap_or_default()
}

fn do_send(pane: &str, sanitized: &str) -> Result<bool> {
    let before = capture_pane(pane);

    // Paste text via tmux paste-buffer (handles special chars better than send-keys),
    // then send Enter via send-keys (some CLIs don't submit on pasted newlines).
    let mut child = Command::new("tmux")
        .args(["load-buffer", "-"])
        .stdin(Stdio::piped())
        .spawn()
        .context("failed to run tmux load-buffer")?;
    if let Some(mut stdin) = child.stdin.take() {
        use std::io::Write;
        let _ = stdin.write_all(sanitized.as_bytes());
    }
    let status = child.wait().context("tmux load-buffer failed")?;
    if !status.success() {
        bail!("tmux load-buffer failed");
    }

    let status = Command::new("tmux")
        .args(["paste-buffer", "-t", pane])
        .status()
        .context("failed to run tmux paste-buffer")?;
    if !status.success() {
        bail!("tmux paste-buffer failed");
    }

    std::thread::sleep(std::time::Duration::from_millis(200));

    // Send Enter separately — pasted newlines don't always trigger submission
    let _ = Command::new("tmux")
        .args(["send-keys", "-t", pane, "Enter"])
        .status();

    // Brief poll to detect obvious paste failures (for retry logic)
    for _ in 0..8 {
        std::thread::sleep(std::time::Duration::from_millis(500));
        let current = capture_pane(pane);
        if current != before {
            return Ok(true);
        }
    }
    Ok(false)
}

/// Send a message to a tmux pane via paste-buffer. Sanitizes special characters
/// and retries once on failure.
pub fn send_to_pane(pane: &str, message: &str) -> Result<()> {
    let sanitized: String = message
        .replace('!', "\u{FF01}")
        .split_whitespace()
        .collect::<Vec<_>>()
        .join(" ");

    // First attempt
    if do_send(pane, &sanitized)? {
        return Ok(());
    }

    // Retry once
    eprintln!("webact ipc: first send to {pane} saw no pane change, retrying...");
    let _ = do_send(pane, &sanitized)?;
    Ok(())
}

// --- Socket path ---

/// Socket path for this webact instance.
pub fn socket_path(unique_pane_id: &str) -> std::path::PathBuf {
    std::path::PathBuf::from(format!("/tmp/webact-{unique_pane_id}.sock"))
}

/// Clean up a stale socket file.
fn cleanup_stale_socket(path: &std::path::Path) {
    if path.exists() {
        match std::os::unix::net::UnixStream::connect(path) {
            Ok(_) => {
                eprintln!("webact ipc: socket {} is in use by another process", path.display());
            }
            Err(_) => {
                let _ = std::fs::remove_file(path);
            }
        }
    }
}

// --- Socket listener ---

/// Start the IPC socket listener in a background thread.
/// Returns the socket path for cleanup.
pub fn start_socket_listener(
    unique_pane_id: &str,
    display_pane: &str,
    session: &str,
    agent_name: &str,
    agent_nick: Option<&str>,
) -> Result<std::path::PathBuf> {
    let path = socket_path(unique_pane_id);
    cleanup_stale_socket(&path);

    let listener = UnixListener::bind(&path)
        .with_context(|| format!("failed to bind IPC socket at {}", path.display()))?;

    {
        use std::os::unix::fs::PermissionsExt;
        let _ = std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o600));
    }

    eprintln!("webact ipc: socket listening at {}", path.display());

    let name = agent_name.to_string();
    let nick = agent_nick.map(|n| n.to_string());
    let sess = session.to_string();
    let pane = display_pane.to_string();

    std::thread::spawn(move || {
        let mut last_paste = std::time::Instant::now() - IPC_PASTE_COOLDOWN;

        for stream in listener.incoming() {
            let mut stream = match stream {
                Ok(s) => s,
                Err(e) => {
                    eprintln!("webact ipc: accept error: {e}");
                    continue;
                }
            };

            let mut buf = vec![0u8; IPC_MAX_MESSAGE_SIZE + 512];
            let n = match stream.read(&mut buf) {
                Ok(n) if n > 0 => n,
                _ => continue,
            };

            let request: serde_json::Value = match serde_json::from_slice(&buf[..n]) {
                Ok(v) => v,
                Err(_) => {
                    let err = json!({
                        "jsonrpc": "2.0",
                        "id": serde_json::Value::Null,
                        "error": { "code": -32700, "message": "Parse error" }
                    });
                    let _ = stream.write_all(
                        serde_json::to_string(&err).unwrap_or_default().as_bytes(),
                    );
                    continue;
                }
            };

            let id = request.get("id").cloned();
            let method = request
                .get("method")
                .and_then(Value::as_str)
                .unwrap_or_default();

            let response = match method {
                "who" => {
                    let mut result = json!({
                        "agent": name,
                        "session": sess,
                        "pane": pane,
                        "version": IPC_PROTOCOL_VERSION,
                        "type": "webact"
                    });
                    if let Some(ref n) = nick {
                        result["nick"] = json!(n);
                    }
                    json!({
                        "jsonrpc": "2.0",
                        "id": id,
                        "result": result
                    })
                }
                "send" => {
                    let params = request.get("params").cloned().unwrap_or(Value::Null);
                    let message = params
                        .get("message")
                        .and_then(Value::as_str)
                        .unwrap_or_default();
                    let from = params
                        .get("from")
                        .and_then(Value::as_str)
                        .unwrap_or("unknown");

                    if message.is_empty() {
                        json!({
                            "jsonrpc": "2.0",
                            "id": id,
                            "error": { "code": -32602, "message": "Missing 'message' parameter" }
                        })
                    } else if message.len() > IPC_MAX_MESSAGE_SIZE {
                        json!({
                            "jsonrpc": "2.0",
                            "id": id,
                            "error": { "code": -32602, "message": format!("Message exceeds {}B limit", IPC_MAX_MESSAGE_SIZE) }
                        })
                    } else {
                        // Rate limit pastes
                        let elapsed = last_paste.elapsed();
                        if elapsed < IPC_PASTE_COOLDOWN {
                            std::thread::sleep(IPC_PASTE_COOLDOWN - elapsed);
                        }

                        // Message is already formatted by the sender (e.g. "[message from X]: ...")
                        match send_to_pane(&pane, message) {
                            Ok(()) => {
                                eprintln!("webact ipc: message from {from} delivered");
                                last_paste = std::time::Instant::now();
                                json!({
                                    "jsonrpc": "2.0",
                                    "id": id,
                                    "result": { "ok": true }
                                })
                            }
                            Err(e) => {
                                eprintln!("webact ipc: delivery failed: {e}");
                                last_paste = std::time::Instant::now();
                                json!({
                                    "jsonrpc": "2.0",
                                    "id": id,
                                    "error": { "code": -32000, "message": format!("Delivery failed: {e}") }
                                })
                            }
                        }
                    }
                }
                _ => json!({
                    "jsonrpc": "2.0",
                    "id": id,
                    "error": { "code": -32601, "message": format!("Method not found: {method}") }
                }),
            };

            let _ = stream
                .write_all(serde_json::to_string(&response).unwrap_or_default().as_bytes());
        }
    });

    Ok(path)
}

// --- Socket client ---

/// Query an agent's identity via its IPC socket.
pub fn ipc_query_who(path: &std::path::Path) -> Option<serde_json::Value> {
    let mut stream = std::os::unix::net::UnixStream::connect(path).ok()?;
    stream
        .set_read_timeout(Some(Duration::from_secs(2)))
        .ok()?;
    let request = json!({"jsonrpc": "2.0", "method": "who", "id": 1});
    stream
        .write_all(serde_json::to_string(&request).ok()?.as_bytes())
        .ok()?;
    let mut buf = vec![0u8; 1024];
    let n = stream.read(&mut buf).ok()?;
    let response: serde_json::Value = serde_json::from_slice(&buf[..n]).ok()?;
    response.get("result").cloned()
}

/// Send a message to an agent via its IPC socket.
pub fn ipc_send_message(
    socket_path: &std::path::Path,
    message: &str,
    from: &str,
) -> Result<()> {
    let mut stream = std::os::unix::net::UnixStream::connect(socket_path)
        .with_context(|| {
            format!(
                "failed to connect to IPC socket at {}",
                socket_path.display()
            )
        })?;
    stream
        .set_read_timeout(Some(Duration::from_secs(30)))
        .ok();
    let request = json!({
        "jsonrpc": "2.0",
        "method": "send",
        "params": { "message": message, "from": from },
        "id": 1
    });
    stream.write_all(serde_json::to_string(&request)?.as_bytes())?;

    let mut buf = vec![0u8; 1024];
    let n = stream
        .read(&mut buf)
        .context("no response from IPC socket")?;
    let response: serde_json::Value = serde_json::from_slice(&buf[..n])?;
    if let Some(err) = response.get("error") {
        let msg = err
            .get("message")
            .and_then(Value::as_str)
            .unwrap_or("unknown error");
        bail!("{msg}");
    }
    Ok(())
}

/// Discover all agents across sessions by scanning IPC sockets.
/// Scans both webact-% and agentbus-% socket patterns.
pub fn discover_all_agents() -> Vec<(std::path::PathBuf, serde_json::Value)> {
    let mut agents = Vec::new();
    if let Ok(entries) = std::fs::read_dir("/tmp") {
        for entry in entries.flatten() {
            let name = entry.file_name();
            let name = name.to_string_lossy();
            let is_agent_socket = (name.starts_with("webact-%") || name.starts_with("agentbus-%"))
                && name.ends_with(".sock");
            if is_agent_socket {
                let path = entry.path();
                if let Some(info) = ipc_query_who(&path) {
                    agents.push((path, info));
                } else {
                    // Stale socket — clean up
                    let _ = std::fs::remove_file(&path);
                }
            }
        }
    }
    agents
}

/// Find an agent's socket by name across all sessions.
/// Find an agent's socket by name or nickname across all sessions.
pub fn find_agent_socket(target: &str) -> Option<std::path::PathBuf> {
    discover_all_agents()
        .into_iter()
        .find(|(_, info)| {
            info.get("agent").and_then(Value::as_str) == Some(target)
                || info.get("nick").and_then(Value::as_str) == Some(target)
        })
        .map(|(path, _)| path)
}

/// Find the IPC socket associated with a specific tmux pane.
/// Checks both webact-% and agentbus-% patterns.
pub fn find_socket_for_pane(pane_unique_id: &str) -> Option<std::path::PathBuf> {
    // Check webact socket first
    let webact_path = std::path::PathBuf::from(format!("/tmp/webact-{pane_unique_id}.sock"));
    if webact_path.exists() {
        return Some(webact_path);
    }
    // Check agentbus socket
    let agentbus_path = std::path::PathBuf::from(format!("/tmp/agentbus-{pane_unique_id}.sock"));
    if agentbus_path.exists() {
        return Some(agentbus_path);
    }
    // Scan all sockets and query for the pane
    discover_all_agents()
        .into_iter()
        .find(|(_, info)| {
            info.get("pane")
                .and_then(Value::as_str)
                .map(|p| p == pane_unique_id || p.ends_with(&format!(".{}", pane_unique_id)))
                .unwrap_or(false)
        })
        .map(|(path, _)| path)
}

// --- MCP tool handlers ---

/// Handle the `who` tool — discover all agents.
pub fn cmd_who(ctx: &mut crate::AppContext) -> Result<()> {
    let agents = discover_all_agents();
    if agents.is_empty() {
        out!(ctx, "No agents discovered. (Are any agents running in tmux with webact?)");
        return Ok(());
    }
    let mut lines = Vec::new();
    for (path, info) in &agents {
        let name = info.get("agent").and_then(Value::as_str).unwrap_or("?");
        let nick = info.get("nick").and_then(Value::as_str);
        let session = info.get("session").and_then(Value::as_str).unwrap_or("?");
        let pane = info.get("pane").and_then(Value::as_str).unwrap_or("?");
        let agent_type = info.get("type").and_then(Value::as_str).unwrap_or("unknown");
        let socket = path.file_name().and_then(|n| n.to_str()).unwrap_or("?");
        let nick_str = nick.map(|n| format!(" \"{n}\"")).unwrap_or_default();
        lines.push(format!("- {name}{nick_str} (session \"{session}\", pane {pane}, type: {agent_type}, socket: {socket})"));
    }
    out!(ctx, "Agents discovered:\n{}", lines.join("\n"));
    Ok(())
}

/// Handle the `send_message` tool — send a message to an agent by name.
pub fn cmd_send_message(ctx: &mut crate::AppContext, to: &str, message: &str) -> Result<()> {
    let pane = detect_tmux_pane();
    let my_name = pane
        .as_ref()
        .map(|p| format!("webact@{}", p.display_id))
        .unwrap_or_else(|| "webact".to_string());

    match find_agent_socket(to) {
        Some(socket_path) => {
            let full_message = format!("[message from {my_name}]: {message}");
            ipc_send_message(&socket_path, &full_message, &my_name)?;
            out!(ctx, "Message sent to {to}.");
            Ok(())
        }
        None => {
            let agents = discover_all_agents();
            let available: Vec<&str> = agents
                .iter()
                .filter_map(|(_, info)| info.get("agent").and_then(Value::as_str))
                .collect();
            if available.is_empty() {
                bail!("Agent \"{to}\" not found. No agents discovered.");
            } else {
                bail!("Agent \"{to}\" not found. Available: {}", available.join(", "));
            }
        }
    }
}
