import ApplicationServices
import Foundation

/// Find the first element matching query and click it.
/// Returns a DesktopClickResult describing what happened.
func clickElement(pid: Int32, query: String) -> DesktopClickResult {
    let matches = findElements(pid: pid, query: query)

    guard let first = matches.first else {
        return DesktopClickResult(kind: "notFound", role: nil, title: nil, x: nil, y: nil)
    }

    // Try to resolve the AX element and press it
    let appElement = AXUIElementCreateApplication(pid)
    if let element = resolveElement(root: appElement, path: first.path) {
        // Check if AXPress is available
        var actionsRef: CFArray?
        AXUIElementCopyActionNames(element, &actionsRef)
        let actions = (actionsRef as? [String]) ?? []

        if actions.contains(kAXPressAction as String) {
            let result = AXUIElementPerformAction(element, kAXPressAction as CFString)
            if result == .success {
                return DesktopClickResult(
                    kind: "axPress",
                    role: first.role,
                    title: first.title,
                    x: nil,
                    y: nil
                )
            }
        }
    }

    // Fallback: return coordinates for enigo click
    if let frame = first.frame {
        let centerX = frame.x + frame.width / 2.0
        let centerY = frame.y + frame.height / 2.0
        return DesktopClickResult(
            kind: "fallbackClick",
            role: first.role,
            title: first.title,
            x: centerX,
            y: centerY
        )
    }

    return DesktopClickResult(kind: "noFrame", role: first.role, title: first.title, x: nil, y: nil)
}

/// Walk the AX tree following a DesktopElementPath to find the actual AXUIElement.
private func resolveElement(root: AXUIElement, path: DesktopElementPath) -> AXUIElement? {
    var current = root

    for step in path.chain {
        var childrenRef: CFTypeRef?
        let result = AXUIElementCopyAttributeValue(current, kAXChildrenAttribute as CFString, &childrenRef)
        guard result == .success, let children = childrenRef as? [AXUIElement] else {
            return nil
        }

        // Try to find by role + title + index
        var found = false
        for child in children {
            let role = axStringAttribute(child, kAXRoleAttribute) ?? ""
            let title = axStringAttribute(child, kAXTitleAttribute)

            if role == step.role && title == step.title {
                current = child
                found = true
                break
            }
        }

        // Fallback: use index directly
        if !found {
            guard step.index < children.count else { return nil }
            current = children[step.index]
        }
    }

    return current
}
