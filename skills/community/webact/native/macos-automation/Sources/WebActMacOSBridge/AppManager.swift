import AppKit

func listApps() -> [DesktopAppInfo] {
    let apps = NSWorkspace.shared.runningApplications
    return apps.compactMap { app in
        guard let name = app.localizedName, !name.isEmpty else { return nil }
        // Skip background-only apps (no UI)
        guard app.activationPolicy == .regular else { return nil }
        return DesktopAppInfo(
            pid: app.processIdentifier,
            bundleId: app.bundleIdentifier,
            name: name,
            isActive: app.isActive
        )
    }
}
