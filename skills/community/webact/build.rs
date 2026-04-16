#[cfg(target_os = "macos")]
use swift_rs::SwiftLinker;

fn main() {
    println!("cargo:rerun-if-changed=build.rs");

    #[cfg(target_os = "macos")]
    {
        println!("cargo:rerun-if-changed=native/macos-automation/Package.swift");
        println!("cargo:rerun-if-changed=native/macos-automation/Sources/WebActMacOSBridge");

        SwiftLinker::new("12.3")
            .with_package("WebActMacOSBridge", "native/macos-automation")
            .link();

        println!("cargo:rustc-link-lib=framework=Foundation");
        println!("cargo:rustc-link-lib=framework=AppKit");
        println!("cargo:rustc-link-lib=framework=ApplicationServices");
        println!("cargo:rustc-link-lib=framework=CoreGraphics");
    }
}
