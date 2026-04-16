import Foundation

struct DesktopAppInfo: Codable {
    let pid: Int32
    let bundleId: String?
    let name: String
    let isActive: Bool
}

struct DesktopRect: Codable {
    let x: Double
    let y: Double
    let width: Double
    let height: Double
}

struct DesktopWindowInfo: Codable {
    let pid: Int32
    let windowId: UInt32?
    let title: String?
    let frame: DesktopRect
    let isMain: Bool
    let isFocused: Bool
}

struct DesktopElementStep: Codable {
    let role: String
    let title: String?
    let identifier: String?
    let index: Int
}

struct DesktopElementPath: Codable {
    let pid: Int32
    let chain: [DesktopElementStep]
}

struct DesktopElementMatch: Codable {
    let path: DesktopElementPath
    let role: String
    let title: String?
    let value: String?
    let frame: DesktopRect?
    let actions: [String]
}

struct DesktopClickResult: Codable {
    let kind: String
    let role: String?
    let title: String?
    let x: Double?
    let y: Double?
}

func encodeJSON<T: Encodable>(_ value: T) -> String {
    let encoder = JSONEncoder()
    guard let data = try? encoder.encode(value),
          let str = String(data: data, encoding: .utf8) else {
        return "[]"
    }
    return str
}
