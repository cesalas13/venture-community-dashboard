// Generates a Dock-ready Venture Community icon from workspace-logo.svg.
// The artwork is inset inside a rounded black app tile so it reads like
// a macOS app icon instead of a full-bleed square image.

import Cocoa

let dashDir = URL(fileURLWithPath: CommandLine.arguments[0])
    .deletingLastPathComponent()
    .deletingLastPathComponent()
let sourceURL = dashDir.appendingPathComponent("workspace-logo.svg")
let outURL = dashDir.appendingPathComponent("vcw-control-icon-1024.png")
let size = NSSize(width: 1024, height: 1024)

guard let logo = NSImage(contentsOf: sourceURL) else {
    FileHandle.standardError.write("missing logo at \(sourceURL.path)\n".data(using: .utf8)!)
    exit(1)
}

let img = NSImage(size: size)
img.lockFocus()

let ctx = NSGraphicsContext.current!.cgContext
ctx.clear(CGRect(origin: .zero, size: size))

let outer = CGRect(x: 72, y: 72, width: 880, height: 880)
let outerPath = CGPath(roundedRect: outer, cornerWidth: 206, cornerHeight: 206, transform: nil)

ctx.saveGState()
ctx.setShadow(offset: CGSize(width: 0, height: -22), blur: 48, color: NSColor.black.withAlphaComponent(0.48).cgColor)
ctx.setFillColor(NSColor(red: 0.006, green: 0.007, blue: 0.009, alpha: 1).cgColor)
ctx.addPath(outerPath)
ctx.fillPath()
ctx.restoreGState()

let glossColors = [
    NSColor.white.withAlphaComponent(0.14).cgColor,
    NSColor.white.withAlphaComponent(0.02).cgColor,
    NSColor.black.withAlphaComponent(0.18).cgColor
]
let gloss = CGGradient(colorsSpace: CGColorSpaceCreateDeviceRGB(),
                       colors: glossColors as CFArray,
                       locations: [0.0, 0.45, 1.0])!
ctx.saveGState()
ctx.addPath(outerPath)
ctx.clip()
ctx.drawLinearGradient(gloss,
                       start: CGPoint(x: outer.midX, y: outer.maxY),
                       end: CGPoint(x: outer.midX, y: outer.minY),
                       options: [])
ctx.restoreGState()

ctx.setStrokeColor(NSColor.white.withAlphaComponent(0.86).cgColor)
ctx.setLineWidth(10)
ctx.addPath(CGPath(roundedRect: outer.insetBy(dx: 5, dy: 5), cornerWidth: 198, cornerHeight: 198, transform: nil))
ctx.strokePath()

ctx.setStrokeColor(NSColor.white.withAlphaComponent(0.20).cgColor)
ctx.setLineWidth(2)
ctx.addPath(CGPath(roundedRect: outer.insetBy(dx: 22, dy: 22), cornerWidth: 178, cornerHeight: 178, transform: nil))
ctx.strokePath()

let inner = CGRect(x: 176, y: 176, width: 672, height: 672)
let innerPath = CGPath(roundedRect: inner, cornerWidth: 104, cornerHeight: 104, transform: nil)

ctx.saveGState()
ctx.setFillColor(NSColor.white.cgColor)
ctx.addPath(innerPath)
ctx.fillPath()
ctx.addPath(innerPath)
ctx.clip()
logo.draw(in: inner, from: .zero, operation: .sourceOver, fraction: 1.0)
ctx.restoreGState()

ctx.setStrokeColor(NSColor.white.withAlphaComponent(0.95).cgColor)
ctx.setLineWidth(12)
ctx.addPath(CGPath(roundedRect: inner.insetBy(dx: -6, dy: -6), cornerWidth: 112, cornerHeight: 112, transform: nil))
ctx.strokePath()

ctx.setStrokeColor(NSColor.black.withAlphaComponent(0.24).cgColor)
ctx.setLineWidth(2)
ctx.addPath(CGPath(roundedRect: inner.insetBy(dx: 8, dy: 8), cornerWidth: 94, cornerHeight: 94, transform: nil))
ctx.strokePath()

img.unlockFocus()

guard let tiff = img.tiffRepresentation,
      let rep = NSBitmapImageRep(data: tiff),
      let png = rep.representation(using: .png, properties: [:]) else {
    FileHandle.standardError.write("failed to encode PNG\n".data(using: .utf8)!)
    exit(1)
}

try! png.write(to: outURL)
print("wrote \(outURL.path) (\(png.count) bytes)")
