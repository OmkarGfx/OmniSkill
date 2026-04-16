import Foundation

struct FindQuery: Codable {
    let query: String
}

func parseQuery(json: UnsafePointer<CChar>?) -> String? {
    guard let json = json else { return nil }
    let str = String(cString: json)
    guard let data = str.data(using: .utf8),
          let parsed = try? JSONDecoder().decode(FindQuery.self, from: data) else {
        return nil
    }
    return parsed.query
}
