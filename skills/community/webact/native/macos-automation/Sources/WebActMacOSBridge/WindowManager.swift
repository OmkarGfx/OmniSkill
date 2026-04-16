import AppKit
import ApplicationServices

func listWindows(pid: Int32) -> [DesktopWindowInfo] {
    let appElement = AXUIElementCreateApplication(pid)

    var windowsRef: CFTypeRef?
    let result = AXUIElementCopyAttributeValue(appElement, kAXWindowsAttribute as CFString, &windowsRef)
    guard result == .success, let windows = windowsRef as? [AXUIElement] else {
        return []
    }

    return windows.enumerated().compactMap { (index, window) in
        let title = axStringAttribute(window, kAXTitleAttribute)
        let position = axPointAttribute(window, kAXPositionAttribute)
        let size = axSizeAttribute(window, kAXSizeAttribute)
        let isMain = axBoolAttribute(window, kAXMainAttribute)
        let isFocused = axBoolAttribute(window, kAXFocusedAttribute)

        let frame = DesktopRect(
            x: Double(position?.x ?? 0),
            y: Double(position?.y ?? 0),
            width: Double(size?.width ?? 0),
            height: Double(size?.height ?? 0)
        )

        // _AXUIElementGetWindow is a private API and may not be available
        let windowId: UInt32? = nil

        return DesktopWindowInfo(
            pid: pid,
            windowId: windowId,
            title: title,
            frame: frame,
            isMain: isMain,
            isFocused: isFocused
        )
    }
}

// MARK: - AX Attribute Helpers

func axStringAttribute(_ element: AXUIElement, _ attribute: String) -> String? {
    var ref: CFTypeRef?
    guard AXUIElementCopyAttributeValue(element, attribute as CFString, &ref) == .success else {
        return nil
    }
    return ref as? String
}

func axBoolAttribute(_ element: AXUIElement, _ attribute: String) -> Bool {
    var ref: CFTypeRef?
    guard AXUIElementCopyAttributeValue(element, attribute as CFString, &ref) == .success else {
        return false
    }
    if let num = ref as? NSNumber {
        return num.boolValue
    }
    return false
}

func axPointAttribute(_ element: AXUIElement, _ attribute: String) -> CGPoint? {
    var ref: CFTypeRef?
    guard AXUIElementCopyAttributeValue(element, attribute as CFString, &ref) == .success else {
        return nil
    }
    var point = CGPoint.zero
    guard AXValueGetValue(ref as! AXValue, .cgPoint, &point) else {
        return nil
    }
    return point
}

func axSizeAttribute(_ element: AXUIElement, _ attribute: String) -> CGSize? {
    var ref: CFTypeRef?
    guard AXUIElementCopyAttributeValue(element, attribute as CFString, &ref) == .success else {
        return nil
    }
    var size = CGSize.zero
    guard AXValueGetValue(ref as! AXValue, .cgSize, &size) else {
        return nil
    }
    return size
}
