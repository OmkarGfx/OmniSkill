import ApplicationServices
import Foundation

/// Walk the AX tree for an app rooted at the given pid.
/// Returns all elements matching the query (case-insensitive substring).
func findElements(pid: Int32, query: String) -> [DesktopElementMatch] {
    let appElement = AXUIElementCreateApplication(pid)
    var matches: [DesktopElementMatch] = []
    let lowerQuery = query.lowercased()

    walkTree(
        element: appElement,
        pid: pid,
        chain: [],
        siblingIndex: 0,
        depth: 0,
        maxDepth: 12,
        query: lowerQuery,
        matches: &matches
    )

    return matches
}

private func walkTree(
    element: AXUIElement,
    pid: Int32,
    chain: [DesktopElementStep],
    siblingIndex: Int,
    depth: Int,
    maxDepth: Int,
    query: String,
    matches: inout [DesktopElementMatch]
) {
    guard depth < maxDepth else { return }
    // Bail early if we have enough matches
    guard matches.count < 50 else { return }

    let role = axStringAttribute(element, kAXRoleAttribute) ?? "AXUnknown"
    let title = axStringAttribute(element, kAXTitleAttribute)
    let value: String? = axStringAttribute(element, kAXValueAttribute)
    let identifier = axStringAttribute(element, kAXIdentifierAttribute)

    let step = DesktopElementStep(
        role: role,
        title: title,
        identifier: identifier,
        index: siblingIndex
    )
    let currentChain = chain + [step]

    // Check if this element matches the query
    let searchable = [
        role.lowercased(),
        title?.lowercased() ?? "",
        value?.lowercased() ?? "",
        identifier?.lowercased() ?? ""
    ]

    if searchable.contains(where: { $0.contains(query) }) {
        let position = axPointAttribute(element, kAXPositionAttribute)
        let size = axSizeAttribute(element, kAXSizeAttribute)

        var frame: DesktopRect? = nil
        if let pos = position, let sz = size {
            frame = DesktopRect(x: pos.x, y: pos.y, width: sz.width, height: sz.height)
        }

        // Get available actions
        var actionsRef: CFArray?
        AXUIElementCopyActionNames(element, &actionsRef)
        let actions = (actionsRef as? [String]) ?? []

        let path = DesktopElementPath(pid: pid, chain: currentChain)
        let match = DesktopElementMatch(
            path: path,
            role: role,
            title: title,
            value: value.map { String($0.prefix(200)) },
            frame: frame,
            actions: actions
        )
        matches.append(match)
    }

    // Recurse into children
    var childrenRef: CFTypeRef?
    let result = AXUIElementCopyAttributeValue(element, kAXChildrenAttribute as CFString, &childrenRef)
    guard result == .success, let children = childrenRef as? [AXUIElement] else {
        return
    }

    for (index, child) in children.enumerated() {
        walkTree(
            element: child,
            pid: pid,
            chain: currentChain,
            siblingIndex: index,
            depth: depth + 1,
            maxDepth: maxDepth,
            query: query,
            matches: &matches
        )
    }
}
