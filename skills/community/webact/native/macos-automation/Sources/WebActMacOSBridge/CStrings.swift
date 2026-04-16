import Foundation

func makeCString(_ string: String) -> UnsafeMutablePointer<CChar>? {
    strdup(string)
}

@_cdecl("weba_macos_free_string")
public func weba_macos_free_string(_ ptr: UnsafeMutablePointer<CChar>?) {
    free(ptr)
}
