import Foundation

@_cdecl("weba_macos_list_apps_json")
public func weba_macos_list_apps_json() -> UnsafeMutablePointer<CChar>? {
    let apps = listApps()
    return makeCString(encodeJSON(apps))
}

@_cdecl("weba_macos_list_windows_json")
public func weba_macos_list_windows_json(_ pid: Int32) -> UnsafeMutablePointer<CChar>? {
    let windows = listWindows(pid: pid)
    return makeCString(encodeJSON(windows))
}

@_cdecl("weba_macos_find_json")
public func weba_macos_find_json(_ pid: Int32, _ queryJson: UnsafePointer<CChar>?) -> UnsafeMutablePointer<CChar>? {
    guard let query = parseQuery(json: queryJson), !query.isEmpty else {
        return makeCString("[]")
    }
    let matches = findElements(pid: pid, query: query)
    return makeCString(encodeJSON(matches))
}

@_cdecl("weba_macos_click_json")
public func weba_macos_click_json(_ pid: Int32, _ queryJson: UnsafePointer<CChar>?) -> UnsafeMutablePointer<CChar>? {
    guard let query = parseQuery(json: queryJson), !query.isEmpty else {
        return makeCString(encodeJSON(DesktopClickResult(kind: "noQuery", role: nil, title: nil, x: nil, y: nil)))
    }
    let result = clickElement(pid: pid, query: query)
    return makeCString(encodeJSON(result))
}
