import Cocoa
import WebKit

final class AppDelegate: NSObject, NSApplicationDelegate, WKNavigationDelegate, WKUIDelegate, WKScriptMessageHandler {
    var window: NSWindow!
    var webView: WKWebView!

    let label = "io.example.workspace-dashboard.server"
    let plist = FileManager.default.homeDirectoryForCurrentUser
        .appendingPathComponent("Library/LaunchAgents/io.example.workspace-dashboard.server.plist")
        .path
    let url = URL(string: "http://127.0.0.1:8766/index.html#/home")!

    func applicationDidFinishLaunching(_ notification: Notification) {
        ensureServer()
        buildWindow()
        loadDashboard()
    }

    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool { false }

    func applicationShouldHandleReopen(_ sender: NSApplication, hasVisibleWindows flag: Bool) -> Bool {
        centerWindow()
        if !flag { window.makeKeyAndOrderFront(nil) }
        return true
    }

    private func ensureServer() {
        if isPortOpen(8766) { return }
        let uid = getuid()
        _ = run("/bin/launchctl", ["bootstrap", "gui/\(uid)", plist])
        _ = run("/bin/launchctl", ["kickstart", "-k", "gui/\(uid)/\(label)"])
        Thread.sleep(forTimeInterval: 0.8)
    }

    private func buildWindow() {
        let config = WKWebViewConfiguration()
        config.preferences.javaScriptCanOpenWindowsAutomatically = true
        config.userContentController.add(self, name: "openExternal")
        config.userContentController.addUserScript(WKUserScript(
            source: """
            document.addEventListener('click', function(event) {
              var trigger = event.target.closest('[data-native-open-url]');
              if (!trigger) return;
              var url = trigger.getAttribute('data-native-open-url');
              if (!url) return;
              event.preventDefault();
              event.stopPropagation();
              window.webkit.messageHandlers.openExternal.postMessage(url);
            }, true);

            document.addEventListener('click', function(event) {
              var link = event.target.closest('a[href]');
              if (!link) return;
              var href = link.getAttribute('href') || '';
              var externalUrl = href;
              if (href.indexOf('workspace://open?') === 0) {
                try {
                  externalUrl = new URL(href).searchParams.get('url') || '';
                } catch (error) {
                  externalUrl = '';
                }
              }
              if (externalUrl.indexOf('https://docs.google.com/') !== 0) return;
              event.preventDefault();
              event.stopPropagation();
              window.webkit.messageHandlers.openExternal.postMessage(externalUrl);
            }, true);
            """,
            injectionTime: .atDocumentEnd,
            forMainFrameOnly: true
        ))
        webView = WKWebView(frame: .zero, configuration: config)
        webView.navigationDelegate = self
        webView.uiDelegate = self
        webView.allowsBackForwardNavigationGestures = true

        window = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: 1360, height: 900),
            styleMask: [.titled, .closable, .miniaturizable, .resizable],
            backing: .buffered,
            defer: false
        )
        window.title = "Venture Community Workspace Dashboard"
        window.titlebarAppearsTransparent = false
        window.titleVisibility = .visible
        window.isMovableByWindowBackground = true
        window.isReleasedWhenClosed = false
        window.contentView = webView
        centerWindow()
        window.makeKeyAndOrderFront(nil)
        NSApp.activate(ignoringOtherApps: true)
        DispatchQueue.main.async { [weak self] in self?.centerWindow() }
    }

    private func centerWindow() {
        guard let window else { return }
        let screenFrame = (window.screen ?? NSScreen.main)?.visibleFrame ?? NSScreen.screens.first?.visibleFrame ?? .zero
        guard screenFrame != .zero else {
            window.center()
            return
        }
        var frame = window.frame
        frame.origin.x = screenFrame.midX - frame.width / 2
        frame.origin.y = screenFrame.midY - frame.height / 2
        window.setFrame(frame, display: true)
    }

    private func loadDashboard() {
        webView.load(URLRequest(url: url, cachePolicy: .reloadIgnoringLocalCacheData, timeoutInterval: 20))
    }

    func webView(_ webView: WKWebView, decidePolicyFor navigationAction: WKNavigationAction, decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
        guard let target = navigationAction.request.url else {
            decisionHandler(.allow)
            return
        }

        if handleDashboardNavigation(target) {
            decisionHandler(.cancel)
            return
        }

        decisionHandler(.allow)
    }

    func webView(_ webView: WKWebView, createWebViewWith configuration: WKWebViewConfiguration, for navigationAction: WKNavigationAction, windowFeatures: WKWindowFeatures) -> WKWebView? {
        guard let target = navigationAction.request.url else { return nil }
        if handleDashboardNavigation(target) { return nil }
        if navigationAction.targetFrame == nil {
            webView.load(navigationAction.request)
        }
        return nil
    }

    func userContentController(_ userContentController: WKUserContentController, didReceive message: WKScriptMessage) {
        guard message.name == "openExternal",
              let rawURL = message.body as? String,
              let externalURL = URL(string: rawURL) else { return }
        NSWorkspace.shared.open(externalURL)
    }

    private func handleDashboardNavigation(_ target: URL) -> Bool {
        if target.scheme == "workspacedash" {
            handleDashboardURL(target)
            return true
        }

        if target.isFileURL {
            NSWorkspace.shared.open(target)
            return true
        }

        if ["http", "https"].contains(target.scheme), !isLocalDashboardURL(target) {
            NSWorkspace.shared.open(target)
            return true
        }

        return false
    }

    private func isLocalDashboardURL(_ url: URL) -> Bool {
        guard let host = url.host else { return false }
        return host == "127.0.0.1" || host == "localhost"
    }

    private func handleDashboardURL(_ url: URL) {
        if url.host == "open" {
            let rawURL = URLComponents(url: url, resolvingAgainstBaseURL: false)?
                .queryItems?
                .first(where: { $0.name == "url" })?
                .value ?? ""
            if let externalURL = URL(string: rawURL) {
                NSWorkspace.shared.open(externalURL)
            }
            return
        }

        guard url.host == "claude" else { return }
        let prompt = URLComponents(url: url, resolvingAgainstBaseURL: false)?
            .queryItems?
            .first(where: { $0.name == "prompt" })?
            .value ?? ""
        openClaudeCLI(prompt: prompt)
    }

    private func openClaudeCLI(prompt: String) {
        let escapedPrompt = shellQuote(prompt)
        let workspacePath = FileManager.default.homeDirectoryForCurrentUser
            .appendingPathComponent("Projects/workspace-framework")
            .path
        let quotedWorkspacePath = shellQuote(workspacePath)
        let command: String
        if prompt.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
            command = "cd \(quotedWorkspacePath) && claude"
        } else {
            command = "cd \(quotedWorkspacePath) && claude \(escapedPrompt)"
        }

        let script = """
        tell application "Terminal"
          activate
          do script "\(appleScriptEscape(command))"
        end tell
        """

        var error: NSDictionary?
        if let appleScript = NSAppleScript(source: script) {
            appleScript.executeAndReturnError(&error)
        }
    }

    private func shellQuote(_ value: String) -> String {
        "'" + value.replacingOccurrences(of: "'", with: "'\\''") + "'"
    }

    private func appleScriptEscape(_ value: String) -> String {
        value
            .replacingOccurrences(of: "\\", with: "\\\\")
            .replacingOccurrences(of: "\"", with: "\\\"")
    }

    private func isPortOpen(_ port: Int32) -> Bool {
        let sock = socket(AF_INET, SOCK_STREAM, 0)
        if sock < 0 { return false }
        defer { close(sock) }
        var addr = sockaddr_in()
        addr.sin_len = UInt8(MemoryLayout<sockaddr_in>.size)
        addr.sin_family = sa_family_t(AF_INET)
        addr.sin_port = in_port_t(port).bigEndian
        inet_pton(AF_INET, "127.0.0.1", &addr.sin_addr)
        return withUnsafePointer(to: &addr) {
            $0.withMemoryRebound(to: sockaddr.self, capacity: 1) {
                connect(sock, $0, socklen_t(MemoryLayout<sockaddr_in>.size)) == 0
            }
        }
    }

    private func run(_ path: String, _ args: [String]) -> Int32 {
        let p = Process()
        p.executableURL = URL(fileURLWithPath: path)
        p.arguments = args
        p.standardOutput = Pipe()
        p.standardError = Pipe()
        do { try p.run(); p.waitUntilExit(); return p.terminationStatus }
        catch { return -1 }
    }
}

let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate
app.setActivationPolicy(.regular)
app.run()
