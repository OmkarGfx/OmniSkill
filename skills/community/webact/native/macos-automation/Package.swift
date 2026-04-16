// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "WebActMacOSBridge",
    platforms: [
        .macOS(.v13),
    ],
    products: [
        .library(
            name: "WebActMacOSBridge",
            type: .static,
            targets: ["WebActMacOSBridge"]
        ),
    ],
    targets: [
        .target(
            name: "WebActMacOSBridge",
            path: "Sources/WebActMacOSBridge"
        ),
    ]
)
