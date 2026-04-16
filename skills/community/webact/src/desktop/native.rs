#![allow(unused)]

use crate::*;
use crate::desktop::types::*;
use std::ffi::{CStr, CString};

#[cfg(target_os = "macos")]
unsafe extern "C" {
    fn weba_macos_list_apps_json() -> *mut libc::c_char;
    fn weba_macos_list_windows_json(pid: i32) -> *mut libc::c_char;
    fn weba_macos_find_json(pid: i32, query_json: *const libc::c_char) -> *mut libc::c_char;
    fn weba_macos_click_json(pid: i32, query_json: *const libc::c_char) -> *mut libc::c_char;
    fn weba_macos_free_string(ptr: *mut libc::c_char);
}

/// Call a Swift function that returns a JSON string, parse it into T.
#[cfg(target_os = "macos")]
unsafe fn call_swift_json<T: serde::de::DeserializeOwned>(ptr: *mut libc::c_char) -> Result<T> {
    if ptr.is_null() {
        bail!("Swift bridge returned null");
    }
    let cstr = unsafe { CStr::from_ptr(ptr) };
    let json = cstr.to_str().context("invalid UTF-8 from Swift bridge")?;
    let result = serde_json::from_str(json)
        .with_context(|| format!("failed parsing Swift JSON: {json}"))?;
    unsafe { weba_macos_free_string(ptr) };
    Ok(result)
}

#[cfg(target_os = "macos")]
pub fn list_apps() -> Result<Vec<DesktopAppInfo>> {
    unsafe { call_swift_json(weba_macos_list_apps_json()) }
}

#[cfg(target_os = "macos")]
pub fn list_windows(pid: i32) -> Result<Vec<DesktopWindowInfo>> {
    unsafe { call_swift_json(weba_macos_list_windows_json(pid)) }
}

#[cfg(target_os = "macos")]
pub fn find_elements(pid: i32, query: &str) -> Result<Vec<DesktopElementMatch>> {
    let query_json = CString::new(serde_json::to_string(&serde_json::json!({"query": query}))?)
        .context("query contains null byte")?;
    unsafe { call_swift_json(weba_macos_find_json(pid, query_json.as_ptr())) }
}

#[cfg(target_os = "macos")]
pub fn click_element(pid: i32, query: &str) -> Result<DesktopClickResult> {
    let query_json = CString::new(serde_json::to_string(&serde_json::json!({"query": query}))?)
        .context("query contains null byte")?;
    unsafe { call_swift_json(weba_macos_click_json(pid, query_json.as_ptr())) }
}
