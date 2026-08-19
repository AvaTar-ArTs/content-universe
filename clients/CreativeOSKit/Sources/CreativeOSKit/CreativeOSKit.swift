import Foundation

public struct CreativeOSManifest: Codable, Sendable {
    public let id: String
    public let version: String
    public let intent: Intent
    public let scene: Scene
    public struct Intent: Codable, Sendable {
        public let original: String
        public let operation: String?
    }
    public struct Scene: Codable, Sendable {
        public let elements: [Element]
    }
    public struct Element: Codable, Sendable {
        public let id: String
        public let kind: String
        public let label: String
        public let bbox: [Double]
    }
}
