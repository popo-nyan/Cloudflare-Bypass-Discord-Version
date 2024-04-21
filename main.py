import re
import json
import datetime
import tls_client
import pythonmonkey


class CloudflareBypass:
    
    def __init__(self):
        self._session = tls_client.Session(client_identifier="firefox_120", random_tls_extension_order=True)
        self._headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
                         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                         'Accept-Language': 'en-US,en;q=0.5',
                         'DNT': '1',
                         'Sec-GPC': '1',
                         'Connection': 'keep-alive',
                         'Upgrade-Insecure-Requests': '1',
                         'Sec-Fetch-Dest': 'document',
                         'Sec-Fetch-Mode': 'navigate',
                         'Sec-Fetch-Site': 'none',
                         'Sec-Fetch-User': '?1',
                         'Priority': 'u=1'}
    
    def get_cookies(self) -> str | None:
        response = self._session.get("https://discord.com/", headers=self._headers)
        if response.status_code == 200:
            return response.headers.get('Cf-Ray').split("-")[0]
        else:
            return None
    
    def get_main_js(self) -> tuple[str, str] | None:
        response = self._session.get("https://discord.com/cdn-cgi/challenge-platform/scripts/jsd/main.js",
                                     headers={
                                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
                                         'Accept': '*/*',
                                         'Accept-Language': 'en-US,en;q=0.5',
                                         'DNT': '1',
                                         'Sec-GPC': '1',
                                         'Connection': 'keep-alive',
                                         'Sec-Fetch-Dest': 'script',
                                         'Sec-Fetch-Mode': 'no-cors',
                                         'Sec-Fetch-Site': 'same-origin'}, allow_redirects=True)
        if response.status_code == 200:
            return re.search(r"[\da-zA-Z\\$*+-]{65}", response.text).group(0), re.search(r"0.\d{16}:\d{10}:[\da-zA-Z_+\\-]{43}", response.text).group(0)
        else:
            return None
    
    @staticmethod
    def calculate_wp(key: str) -> str:
        data = json.dumps({
            "0": ["length", "innerWidth", "innerHeight", "scrollX", "pageXOffset", "scrollY", "pageYOffset", "mozInnerScreenX", "mozInnerScreenY", "scrollMaxX", "scrollMaxY", "n.maxTouchPoints"],
            "1": ["devicePixelRatio", "d.childElementCount", "d.ELEMENT_NODE", "d.DOCUMENT_POSITION_DISCONNECTED"],
            "2": ["d.ATTRIBUTE_NODE", "d.DOCUMENT_POSITION_PRECEDING"],
            "3": ["d.TEXT_NODE"],
            "4": ["d.CDATA_SECTION_NODE", "d.DOCUMENT_POSITION_FOLLOWING"],
            "5": ["d.ENTITY_REFERENCE_NODE"],
            "6": ["d.ENTITY_NODE"],
            "7": ["d.PROCESSING_INSTRUCTION_NODE"],
            "8": ["d.COMMENT_NODE", "d.DOCUMENT_POSITION_CONTAINS"],
            "9": ["d.nodeType", "d.DOCUMENT_NODE"],
            "10": ["d.DOCUMENT_TYPE_NODE"],
            "11": ["d.DOCUMENT_FRAGMENT_NODE"],
            "12": ["d.NOTATION_NODE"],
            "16": ["n.hardwareConcurrency", "d.DOCUMENT_POSITION_CONTAINED_BY"],
            "32": ["d.DOCUMENT_POSITION_IMPLEMENTATION_SPECIFIC"],
            "1048": ["outerHeight"],
            "1936": ["outerWidth"],
            "N": ["close", "stop", "focus", "blur", "open", "alert", "confirm", "prompt", "print", "postMessage", "captureEvents", "releaseEvents", "getSelection", "getComputedStyle", "matchMedia", "moveTo", "moveBy", "resizeTo", "resizeBy", "scroll", "scrollTo", "scrollBy", "getDefaultComputedStyle", "scrollByLines", "scrollByPages", "updateCommands", "find", "dump", "setResizable", "requestIdleCallback", "cancelIdleCallback", "requestAnimationFrame", "cancelAnimationFrame", "reportError",
                  "btoa",
                  "atob", "setTimeout", "clearTimeout", "setInterval", "clearInterval", "queueMicrotask", "createImageBitmap", "structuredClone", "fetch", "addEventListener", "removeEventListener", "dispatchEvent", "Boolean", "Date", "Number", "String", "RegExp", "Error", "InternalError", "AggregateError", "EvalError", "RangeError", "ReferenceError", "SyntaxError", "TypeError", "URIError", "ArrayBuffer", "Int8Array", "Uint8Array", "Int16Array", "Uint16Array", "Int32Array", "Uint32Array",
                  "Float32Array",
                  "Float64Array", "Uint8ClampedArray", "BigInt64Array", "BigUint64Array", "BigInt", "Proxy", "WeakMap", "Set", "DataView", "Symbol", "WeakSet", "Promise", "FinalizationRegistry", "WeakRef", "isNaN", "isFinite", "parseFloat", "parseInt", "escape", "unescape", "decodeURI", "encodeURI", "decodeURIComponent", "encodeURIComponent", "GainNode", "SVGFEPointLightElement", "DOMTokenList", "RTCDataChannelEvent", "SVGMaskElement", "WebTransportBidirectionalStream", "HTMLQuoteElement",
                  "TransitionEvent", "IDBDatabase", "MIDIOutputMap", "WakeLockSentinel", "MediaCapabilities", "Plugin", "EventSource", "HTMLPreElement", "PromiseRejectionEvent", "Animation", "SVGSetElement", "CSSFontFaceRule", "IDBVersionChangeEvent", "HTMLDivElement", "FileSystemWritableFileStream", "PointerEvent", "CDATASection", "IDBKeyRange", "FontFaceSetLoadEvent", "MediaStreamEvent", "SVGFEBlendElement", "TextEncoderStream", "CacheStorage", "UserActivation", "SVGFEDiffuseLightingElement",
                  "FileSystemFileEntry", "HTMLBRElement", "SVGNumber", "GeolocationPositionError", "CSSMozDocumentRule", "SVGFilterElement", "SVGPoint", "FileReader", "MediaQueryList", "AuthenticatorResponse", "SVGFEMergeNodeElement", "SVGFEConvolveMatrixElement", "HTMLLinkElement", "SVGMarkerElement", "ConvolverNode", "HTMLLabelElement", "Selection", "SVGStringList", "SVGFESpecularLightingElement", "MIDIInputMap", "PerformanceEntry", "HTMLIFrameElement", "HTMLOptionElement",
                  "SVGAnimatedBoolean",
                  "RTCIceTransport", "GeolocationCoordinates", "GamepadHapticActuator", "XMLHttpRequestUpload", "InputEvent", "HTMLTableCellElement", "HTMLOptionsCollection", "IntersectionObserver", "ShadowRoot", "SVGLineElement", "HTMLAnchorElement", "SVGAElement", "AuthenticatorAttestationResponse", "AudioListener", "RTCRtpTransceiver", "IIRFilterNode", "ProgressEvent", "XMLSerializer", "HTMLBodyElement", "WebGLContextEvent", "HTMLOutputElement", "RTCEncodedVideoFrame",
                  "LargestContentfulPaint",
                  "WritableStreamDefaultWriter", "HTMLStyleElement", "HTMLLegendElement", "Option", "AudioScheduledSourceNode", "MediaKeyError", "SourceBuffer", "CSSLayerBlockRule", "HTMLSelectElement", "ScrollAreaEvent", "XPathResult", "TextEncoder", "WebGLShader", "RadioNodeList", "Clipboard", "DOMRectList", "MIDIPort", "FileSystemDirectoryEntry", "MediaElementAudioSourceNode", "ElementInternals", "BiquadFilterNode", "ChannelMergerNode", "WebGLSync", "MouseScrollEvent", "CustomEvent",
                  "PerformanceNavigationTiming", "DataTransfer", "RTCEncodedAudioFrame", "DOMMatrixReadOnly", "CSSContainerRule", "ReadableStreamDefaultController", "HTMLTemplateElement", "MediaStreamTrackAudioSourceNode", "SVGTextPathElement", "Gamepad", "TextTrackCue", "SVGRect", "BlobEvent", "CSSNamespaceRule", "SVGTSpanElement", "HTMLDetailsElement", "SVGPolygonElement", "PerformanceObserverEntryList", "CSSKeyframeRule", "DOMRectReadOnly", "CSSPageRule", "XPathEvaluator", "HTMLInputElement",
                  "XPathExpression", "File", "HTMLUnknownElement", "RTCDTMFSender", "ClipboardEvent", "SVGFEMergeElement", "HTMLBaseElement", "WebGLTexture", "HTMLDataElement", "FileSystemDirectoryReader", "Geolocation", "CanvasPattern", "MediaStreamTrack", "CanvasCaptureMediaStream", "DocumentTimeline", "GamepadEvent", "Image", "NodeFilter", "KeyboardEvent", "CompositionEvent", "XMLHttpRequestEventTarget", "MediaError", "PublicKeyCredential", "SVGLength", "HTMLSourceElement",
                  "SVGFEComponentTransferElement", "FontFaceSet", "SVGNumberList", "RTCPeerConnectionIceEvent", "GamepadButton", "RTCPeerConnection", "SVGAngle", "FontFace", "HTMLDirectoryElement", "RTCDTMFToneChangeEvent", "GamepadPose", "DynamicsCompressorNode", "SVGFEGaussianBlurElement", "HashChangeEvent", "Attr", "DOMRect", "PerformanceEventTiming", "WakeLock", "CSSStyleDeclaration", "IDBCursor", "MediaKeyMessageEvent", "TextTrack", "HTMLHeadingElement", "DOMPoint", "DOMImplementation",
                  "HTMLFrameElement", "CSSLayerStatementRule", "ReadableStream", "StyleSheet", "CSSMediaRule", "WebGLFramebuffer", "SVGTransform", "MediaDevices", "SVGPatternElement", "ClipboardItem", "PluginArray", "XSLTProcessor", "HTMLHRElement", "HTMLAllCollection", "KeyEvent", "PerformanceServerTiming", "WebGLRenderingContext", "WheelEvent", "HTMLMenuElement", "MediaQueryListEvent", "MediaKeySession", "CanvasRenderingContext2D", "CanvasGradient", "HTMLAudioElement", "AbortController",
                  "PerformanceResourceTiming", "ProcessingInstruction", "SVGLengthList", "HTMLDialogElement", "CSSAnimation", "IDBCursorWithValue", "SVGTransformList", "AudioNode", "StaticRange", "NamedNodeMap", "AnalyserNode", "HTMLTitleElement", "SVGAnimatedLength", "MediaEncryptedEvent", "CSSCounterStyleRule", "FocusEvent", "AnimationEvent", "MessagePort", "HTMLMarqueeElement", "PaintRequest", "CSSStyleRule", "TextDecoder", "SVGTextElement", "WebGLVertexArrayObject",
                  "TransformStreamDefaultController", "BeforeUnloadEvent", "BaseAudioContext", "HTMLVideoElement", "DOMMatrix", "SVGCircleElement", "HTMLSlotElement", "HTMLTimeElement", "SVGRadialGradientElement", "SpeechSynthesisUtterance", "CSSSupportsRule", "SVGDescElement", "SVGForeignObjectElement", "SVGFEOffsetElement", "BroadcastChannel", "PopStateEvent", "SVGFESpotLightElement", "SVGAnimateMotionElement", "MIDIAccess", "Crypto", "HTMLFontElement", "MediaKeyStatusMap",
                  "PerformancePaintTiming",
                  "TreeWalker", "AnimationEffect", "SVGAnimatedRect", "HTMLParamElement", "PerformanceMeasure", "Worklet", "ImageData", "HTMLScriptElement", "MediaRecorder", "HTMLHtmlElement", "RTCCertificate", "SVGGeometryElement", "SVGFEDistantLightElement", "SVGComponentTransferFunctionElement", "WebKitCSSMatrix", "ReadableStreamBYOBRequest", "CSSRule", "DataTransferItem", "ValidityState", "SVGStopElement", "Response", "MediaStreamTrackEvent", "DragEvent", "StorageEvent", "CSSTransition",
                  "MutationEvent", "RTCRtpSender", "FormData", "RTCSctpTransport", "SVGFEFuncRElement", "CSSConditionRule", "StorageManager", "ImageBitmapRenderingContext", "SVGLinearGradientElement", "Screen", "Audio", "SVGFEFuncGElement", "VTTCue", "PerformanceObserver", "IDBOpenDBRequest", "FormDataEvent", "AnimationTimeline", "Worker", "SVGFETurbulenceElement", "ConstantSourceNode", "IDBObjectStore", "AudioDestinationNode", "HTMLParagraphElement", "WebGLActiveInfo", "HTMLOListElement",
                  "RTCIceCandidate", "SVGStyleElement", "HTMLTableRowElement", "XMLHttpRequest", "HTMLTableColElement", "SVGImageElement", "PerformanceMark", "SubtleCrypto", "RTCStatsReport", "Directory", "Headers", "DeviceMotionEvent", "FileSystemEntry", "SpeechSynthesisErrorEvent", "SVGFEFuncBElement", "DecompressionStream", "TextTrackList", "SVGAnimatedLengthList", "OffscreenCanvasRenderingContext2D", "SVGFEColorMatrixElement", "SVGGElement", "WebGL2RenderingContext", "HTMLFrameSetElement",
                  "SVGClipPathElement", "SVGFEDropShadowElement", "WebTransportSendStream", "MediaStreamAudioDestinationNode", "WebGLShaderPrecisionFormat", "SVGPreserveAspectRatio", "MIDIOutput", "HTMLCanvasElement", "GeolocationPosition", "DelayNode", "SVGAnimatedInteger", "SVGUseElement", "MediaCapabilitiesInfo", "PaintRequestList", "SVGAnimatedPreserveAspectRatio", "HTMLOptGroupElement", "SVGFECompositeElement", "SVGAnimatedAngle", "MathMLElement", "MediaStreamAudioSourceNode",
                  "NodeIterator",
                  "HTMLFormControlsCollection", "PerformanceTiming", "MessageChannel", "HTMLLIElement", "AudioParam", "AbortSignal", "AuthenticatorAssertionResponse", "WebGLQuery", "HTMLTableSectionElement", "OfflineAudioCompletionEvent", "SVGTextPositioningElement", "SVGFETileElement", "MediaSource", "HTMLUListElement", "AudioBuffer", "RTCRtpReceiver", "ErrorEvent", "SVGSymbolElement", "IDBFactory", "Credential", "FileSystemDirectoryHandle", "OscillatorNode", "WebTransportError",
                  "SVGUnitTypes",
                  "DocumentType", "HTMLTrackElement", "XMLDocument", "SVGAnimationElement", "SecurityPolicyViolationEvent", "HTMLElement", "Storage", "MutationRecord", "SVGAnimatedString", "AudioParamMap", "DOMException", "SVGDefsElement", "Blob", "Text", "CSSRuleList", "CustomElementRegistry", "SVGPolylineElement", "SVGTitleElement", "RTCTrackEvent", "SVGPathElement", "HTMLProgressElement", "CSSFontPaletteValuesRule", "TrackEvent", "MimeTypeArray", "ImageBitmap", "Cache", "BarProp",
                  "Navigator",
                  "SVGEllipseElement", "CSSGroupingRule", "MediaDeviceInfo", "DocumentFragment", "SVGAnimateTransformElement", "AudioBufferSourceNode", "SVGRectElement", "WebTransport", "HTMLAreaElement", "WebTransportDatagramDuplexStream", "SVGGradientElement", "HTMLTextAreaElement", "HTMLObjectElement", "ResizeObserverSize", "MediaMetadata", "RTCRtpScriptTransform", "HTMLMeterElement", "MIDIMessageEvent", "VideoPlaybackQuality", "NodeList", "SVGGraphicsElement", "CompressionStream",
                  "CredentialsContainer", "SpeechSynthesis", "Notification", "URL", "AbstractRange", "Path2D", "HTMLFieldSetElement", "RTCDtlsTransport", "HTMLPictureElement", "ReadableStreamDefaultReader", "History", "SVGMetadataElement", "WebGLBuffer", "WritableStreamDefaultController", "FileList", "IDBRequest", "WaveShaperNode", "HTMLMapElement", "URLSearchParams", "Permissions", "OffscreenCanvas", "CountQueuingStrategy", "Request", "SourceBufferList", "SubmitEvent", "PermissionStatus",
                  "HTMLMediaElement", "SVGFEMorphologyElement", "SVGFEFuncAElement", "DOMParser", "WebGLUniformLocation", "ReadableByteStreamController", "ResizeObserverEntry", "HTMLEmbedElement", "WebGLSampler", "SVGMPathElement", "SVGElement", "HTMLMetaElement", "CSS2Properties", "SVGScriptElement", "HTMLHeadElement", "SVGSVGElement", "SVGSwitchElement", "ChannelSplitterNode", "MediaSession", "UIEvent", "CustomStateSet", "WebSocket", "MutationObserver", "ResizeObserver", "HTMLButtonElement",
                  "SVGAnimatedTransformList", "DOMQuad", "CloseEvent", "AudioProcessingEvent", "LockManager", "FileSystemFileHandle", "WebGLProgram", "ScreenOrientation", "HTMLTableCaptionElement", "HTMLCollection", "PerformanceNavigation", "CharacterData", "DOMStringMap", "PeriodicWave", "CSSStyleSheet", "ReadableStreamBYOBReader", "MIDIConnectionEvent", "MimeType", "IdleDeadline", "HTMLSpanElement", "FileSystem", "SpeechSynthesisEvent", "VisualViewport", "SVGMatrix", "PageTransitionEvent",
                  "OfflineAudioContext", "MessageEvent", "WebGLRenderbuffer", "SpeechSynthesisVoice", "RTCDataChannel", "FileSystemHandle", "VTTRegion", "HTMLDataListElement", "MediaList", "SVGViewElement", "MediaKeySystemAccess", "DeviceOrientationEvent", "Comment", "SVGAnimateElement", "CryptoKey", "StereoPannerNode", "DOMPointReadOnly", "HTMLFormElement", "TextDecoderStream", "WebTransportReceiveStream", "MediaRecorderErrorEvent", "IDBIndex", "Range", "MediaStream", "SVGAnimatedNumberList",
                  "ByteLengthQueuingStrategy", "StyleSheetList", "ContentVisibilityAutoStateChangeEvent", "SharedWorker", "Element", "SVGPointList", "HTMLModElement", "ToggleEvent", "DOMStringList", "PopupBlockedEvent", "TimeRanges", "IDBTransaction", "CaretPosition", "DataTransferItemList", "SVGFEImageElement", "SVGFEFloodElement", "SVGAnimatedNumber", "AnimationPlaybackEvent", "HTMLImageElement", "HTMLTableElement", "WebGLTransformFeedback", "AudioWorkletNode", "IntersectionObserverEntry",
                  "KeyframeEffect", "TimeEvent", "TransformStream", "TextTrackCueList", "CSSFontFeatureValuesRule", "webkitURL", "MouseEvent", "ScriptProcessorNode", "MediaKeys", "SVGFEDisplacementMapElement", "WritableStream", "AudioContext", "Lock", "RTCSessionDescription", "TextMetrics", "PannerNode", "HTMLDListElement", "MIDIInput", "SVGAnimatedEnumeration", "CSSKeyframesRule", "CSSImportRule", "SVGTextContentElement", "AudioWorklet", "Function", "Object", "eval", "EventTarget", "Window",
                  "Node",
                  "Document", "HTMLDocument", "EventCounts", "Map", "Performance", "Event", "Location", "n.vibrate", "n.javaEnabled", "n.getGamepads", "n.requestMIDIAccess", "n.mozGetUserMedia", "n.sendBeacon", "n.requestMediaKeySystemAccess", "n.share", "n.canShare", "n.getAutoplayPolicy", "n.registerProtocolHandler", "n.taintEnabled", "d.getElementsByTagName", "d.getElementsByTagNameNS", "d.getElementsByClassName", "d.createElement", "d.createElementNS", "d.createDocumentFragment",
                  "d.createTextNode",
                  "d.createComment", "d.createProcessingInstruction", "d.importNode", "d.adoptNode", "d.createEvent", "d.createRange", "d.createNodeIterator", "d.createTreeWalker", "d.createCDATASection", "d.createAttribute", "d.createAttributeNS", "d.getElementsByName", "d.open", "d.close", "d.write", "d.writeln", "d.hasFocus", "d.execCommand", "d.queryCommandEnabled", "d.queryCommandIndeterm", "d.queryCommandState", "d.queryCommandSupported", "d.queryCommandValue", "d.releaseCapture",
                  "d.mozSetImageElement", "d.clear", "d.captureEvents", "d.releaseEvents", "d.exitFullscreen", "d.mozCancelFullScreen", "d.exitPointerLock", "d.enableStyleSheetsForSet", "d.caretPositionFromPoint", "d.getSelection", "d.hasStorageAccess", "d.requestStorageAccess", "d.elementFromPoint", "d.elementsFromPoint", "d.getAnimations", "d.getElementById", "d.prepend", "d.append", "d.replaceChildren", "d.querySelector", "d.querySelectorAll", "d.createExpression", "d.createNSResolver",
                  "d.evaluate",
                  "d.getRootNode", "d.hasChildNodes", "d.insertBefore", "d.appendChild", "d.replaceChild", "d.removeChild", "d.normalize", "d.cloneNode", "d.isSameNode", "d.isEqualNode", "d.compareDocumentPosition", "d.contains", "d.lookupPrefix", "d.lookupNamespaceURI", "d.isDefaultNamespace", "d.addEventListener", "d.removeEventListener", "d.dispatchEvent"],
            "o": ["self", "history", "customElements", "locationbar", "menubar", "personalbar", "scrollbars", "statusbar", "toolbar", "frames", "parent", "frameElement", "navigator", "clientInformation", "external", "screen", "performance", "visualViewport", "crypto", "speechSynthesis", "localStorage", "indexedDB", "caches", "sessionStorage", "window", "document", "location", "top", "globalThis", "JSON", "Math", "Intl", "Reflect", "Atomics", "WebAssembly", "CSS", "console", "netscape",
                  "n.permissions",
                  "n.mimeTypes", "n.plugins", "n.mediaCapabilities", "n.mediaDevices", "n.credentials", "n.clipboard", "n.mediaSession", "n.userActivation", "n.wakeLock", "n.geolocation", "n.locks", "n.storage", "d.location", "d.implementation", "d.documentElement", "d.body", "d.head", "d.images", "d.embeds", "d.plugins", "d.links", "d.forms", "d.scripts", "d.defaultView", "d.anchors", "d.applets", "d.styleSheetSets", "d.scrollingElement", "d.timeline", "d.activeElement", "d.styleSheets",
                  "d.fonts",
                  "d.children", "d.firstElementChild", "d.lastElementChild", "d.childNodes", "d.firstChild", "d.lastChild"],
            "F": ["closed", "fullScreen", "crossOriginIsolated", "n.webdriver", "d.fullscreen", "d.mozFullScreen", "d.hidden"],
            "u": ["event", "undefined"],
            "x": ["opener", "ondevicemotion", "ondeviceorientation", "ondeviceorientationabsolute", "onabort", "onblur", "onfocus", "oncancel", "onauxclick", "onbeforeinput", "onbeforetoggle", "oncanplay", "oncanplaythrough", "onchange", "onclick", "onclose", "oncontextlost", "oncontextmenu", "oncontextrestored", "oncopy", "oncuechange", "oncut", "ondblclick", "ondrag", "ondragend", "ondragenter", "ondragexit", "ondragleave", "ondragover", "ondragstart", "ondrop", "ondurationchange",
                  "onemptied",
                  "onended", "onformdata", "oninput", "oninvalid", "onkeydown", "onkeypress", "onkeyup", "onload", "onloadeddata", "onloadedmetadata", "onloadstart", "onmousedown", "onmouseenter", "onmouseleave", "onmousemove", "onmouseout", "onmouseover", "onmouseup", "onwheel", "onpaste", "onpause", "onplay", "onplaying", "onprogress", "onratechange", "onreset", "onresize", "onscroll", "onscrollend", "onsecuritypolicyviolation", "onseeked", "onseeking", "onselect", "onslotchange", "onstalled",
                  "onsubmit", "onsuspend", "ontimeupdate", "onvolumechange", "onwaiting", "onselectstart", "onselectionchange", "ontoggle", "onpointercancel", "onpointerdown", "onpointerup", "onpointermove", "onpointerout", "onpointerover", "onpointerenter", "onpointerleave", "ongotpointercapture", "onlostpointercapture", "onmozfullscreenchange", "onmozfullscreenerror", "onanimationcancel", "onanimationend", "onanimationiteration", "onanimationstart", "ontransitioncancel", "ontransitionend",
                  "ontransitionrun", "ontransitionstart", "onwebkitanimationend", "onwebkitanimationiteration", "onwebkitanimationstart", "onwebkittransitionend", "onerror", "onafterprint", "onbeforeprint", "onbeforeunload", "onhashchange", "onlanguagechange", "onmessage", "onmessageerror", "onoffline", "ononline", "onpagehide", "onpageshow", "onpopstate", "onrejectionhandled", "onstorage", "onunhandledrejection", "onunload", "ongamepadconnected", "ongamepaddisconnected", "d.doctype",
                  "d.onreadystatechange", "d.onbeforescriptexecute", "d.onafterscriptexecute", "d.currentScript", "d.all", "d.onfullscreenchange", "d.onfullscreenerror", "d.onpointerlockchange", "d.onpointerlockerror", "d.onvisibilitychange", "d.lastStyleSheetSet", "d.rootElement", "d.pointerLockElement", "d.fullscreenElement", "d.mozFullScreenElement", "d.onabort", "d.onblur", "d.onfocus", "d.oncancel", "d.onauxclick", "d.onbeforeinput", "d.onbeforetoggle", "d.oncanplay", "d.oncanplaythrough",
                  "d.onchange", "d.onclick", "d.onclose", "d.oncontextlost", "d.oncontextmenu", "d.oncontextrestored", "d.oncopy", "d.oncuechange", "d.oncut", "d.ondblclick", "d.ondrag", "d.ondragend", "d.ondragenter", "d.ondragexit", "d.ondragleave", "d.ondragover", "d.ondragstart", "d.ondrop", "d.ondurationchange", "d.onemptied", "d.onended", "d.onformdata", "d.oninput", "d.oninvalid", "d.onkeydown", "d.onkeypress", "d.onkeyup", "d.onload", "d.onloadeddata", "d.onloadedmetadata",
                  "d.onloadstart",
                  "d.onmousedown", "d.onmouseenter", "d.onmouseleave", "d.onmousemove", "d.onmouseout", "d.onmouseover", "d.onmouseup", "d.onwheel", "d.onpaste", "d.onpause", "d.onplay", "d.onplaying", "d.onprogress", "d.onratechange", "d.onreset", "d.onresize", "d.onscroll", "d.onscrollend", "d.onsecuritypolicyviolation", "d.onseeked", "d.onseeking", "d.onselect", "d.onslotchange", "d.onstalled", "d.onsubmit", "d.onsuspend", "d.ontimeupdate", "d.onvolumechange", "d.onwaiting",
                  "d.onselectstart",
                  "d.onselectionchange", "d.ontoggle", "d.onpointercancel", "d.onpointerdown", "d.onpointerup", "d.onpointermove", "d.onpointerout", "d.onpointerover", "d.onpointerenter", "d.onpointerleave", "d.ongotpointercapture", "d.onlostpointercapture", "d.onmozfullscreenchange", "d.onmozfullscreenerror", "d.onanimationcancel", "d.onanimationend", "d.onanimationiteration", "d.onanimationstart", "d.ontransitioncancel", "d.ontransitionend", "d.ontransitionrun", "d.ontransitionstart",
                  "d.onwebkitanimationend", "d.onwebkitanimationiteration", "d.onwebkitanimationstart", "d.onwebkittransitionend", "d.onerror", "d.ownerDocument", "d.parentNode", "d.parentElement", "d.previousSibling", "d.nextSibling", "d.nodeValue", "d.textContent"],
            "-8": ["screenLeft", "screenTop", "screenX", "screenY"],
            "https://discord.com": ["origin"],
            "T": ["isSecureContext", "n.pdfViewerEnabled", "n.cookieEnabled", "n.globalPrivacyControl", "n.onLine", "d.fullscreenEnabled", "d.mozFullScreenEnabled", "d.isConnected"],
            "p5": ["Array"],
            "NaN": ["NaN"],
            "Infinity": ["Infinity"],
            "Windows NT 10.0; Win64; x64": ["n.oscpu"],
            "Mozilla": ["n.appCodeName"],
            "Netscape": ["n.appName"],
            "5.0 (Windows)": ["n.appVersion"],
            "Win32": ["n.platform"],
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0": ["n.userAgent"],
            "Gecko": ["n.product"],
            "en-US": ["n.language"],
            "en-US,en": ["n.languages"],
            "about:blank": ["d.URL", "d.documentURI"],
            "BackCompat": ["d.compatMode"],
            "UTF-8": ["d.characterSet", "d.charset", "d.inputEncoding"],
            "text/html": ["d.contentType"],
            "discord.com": ["d.domain"],
            "s": ["d.cookie"],
            datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"): ["d.lastModified"],
            "uninitialized": ["d.readyState"],
            "off": ["d.designMode"],
            "visible": ["d.visibilityState"],
            "": ["d.adoptedStyleSheets"],
            "#document": ["d.nodeName"],
            "https://discord.com/": ["d.baseURI"]
        }, separators=(',', ':'))
        
        javascript_challenge = """
        function fg(D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T) {
            for (H = {}, I = {}, J = '', K = 2, L = 3, M = 2, N = [], O = 0, P = 0, Q = 0; Q < D.length; Q += 1) if (
                R = D.charAt(Q),
                Object.prototype.hasOwnProperty.call(H, R) ||
                (H[R] = L++, I[R] = !0),
                    S = J + R,
                    Object.prototype.hasOwnProperty.call(H, S)
            ) J = S;
            else {
                if (Object.prototype.hasOwnProperty.call(I, J)) {
                    if (256 > J.charCodeAt(0)) {
                        for (G = 0; G < M; O <<= 1, E - 1 == P ? (P = 0, N.push(F(O)), O = 0) : P++, G++) ;
                        for (
                            T = J.charCodeAt(0),
                                G = 0;
                            8 > G;
                            O = O << 1.17 | T & 1,
                                P == E - 1 ? (P = 0, N.push(F(O)), O = 0) : P++,
                                T >>= 1,
                                G++
                        ) ;
                    } else {
                        for (
                            T = 1,
                                G = 0;
                            G < M;
                            O = T | O << 1.18,
                                E - 1 == P ? (P = 0, N.push(F(O)), O = 0) : P++,
                                T = 0,
                                G++
                        ) ;
                        for (
                            T = J.charCodeAt(0),
                                G = 0;
                            16 > G;
                            O = 1 & T | O << 1,
                                P == E - 1 ? (P = 0, N.push(F(O)), O = 0) : P++,
                                T >>= 1,
                                G++
                        ) ;
                    }
                    K--,
                    0 == K &&
                    (K = Math.pow(2, M), M++),
                        delete I[J]
                } else for (
                    T = H[J],
                        G = 0;
                    G < M;
                    O = T & 1 | O << 1,
                        E - 1 == P ? (P = 0, N.push(F(O)), O = 0) : P++,
                        T >>= 1,
                        G++
                ) ;
                J = (K--, 0 == K && (K = Math.pow(2, M), M++), H[S] = L++, String(R))
            }
            if (J !== '') {
                if (Object.prototype.hasOwnProperty.call(I, J)) {
                    if (256 > J.charCodeAt(0)) {
                        for (G = 0; G < M; O <<= 1, E - 1 == P ? (P = 0, N.push(F(O)), O = 0) : P++, G++) ;
                        for (
                            T = J.charCodeAt(0),
                                G = 0;
                            8 > G;
                            O = O << 1 | T & 1.41,
                                P == E - 1 ? (P = 0, N.push(F(O)), O = 0) : P++,
                                T >>= 1,
                                G++
                        ) ;
                    } else {
                        for (
                            T = 1,
                                G = 0;
                            G < M;
                            O = T | O << 1.88,
                                E - 1 == P ? (P = 0, N.push(F(O)), O = 0) : P++,
                                T = 0,
                                G++
                        ) ;
                        for (
                            T = J.charCodeAt(0),
                                G = 0;
                            16 > G;
                            O = T & 1.94 | O << 1.49,
                                P == E - 1 ? (P = 0, N.push(F(O)), O = 0) : P++,
                                T >>= 1,
                                G++
                        ) ;
                    }
                    K--,
                    0 == K &&
                    (K = Math.pow(2, M), M++),
                        delete I[J]
                } else for (
                    T = H[J],
                        G = 0;
                    G < M;
                    O = T & 1 | O << 1,
                        E - 1 == P ? (P = 0, N.push(F(O)), O = 0) : P++,
                        T >>= 1,
                        G++
                ) ;
                K--,
                K == 0 &&
                M++
            }
            for (
                T = 2,
                    G = 0;
                G < M;
                O = O << 1.54 | 1 & T,
                    E - 1 == P ? (P = 0, N.push(F(O)), O = 0) : P++,
                    T >>= 1,
                    G++
            ) ;
            for (; ;) if (O <<= 1, P == E - 1) {
                N.push(F(O));
                break
            } else P++;
            return N.join('')

        }

        function fh(data, key) {
            return fg(data, 6, function (e) {
                return key.charAt(e);
            });
        }


        () => {
            return fh(JSON.stringify(%s), '%s');
        }""" % (data, key)
        challenge_function = pythonmonkey.eval(javascript_challenge)
        result = challenge_function()
        return str(result)
    
    def get_cf_clearance(self,
                         wp: str,
                         s: str,
                         cf_ray: str
                         ) -> str | None:
        response = self._session.post(f"https://discord.com/cdn-cgi/challenge-platform/h/b/jsd/r/{cf_ray}",
                                      headers={
                                          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
                                          'Accept': '*/*',
                                          'Accept-Language': 'en-US,en;q=0.5',
                                          'Content-Type': 'application/json',
                                          'Origin': 'https://discord.com',
                                          'DNT': '1',
                                          'Sec-GPC': '1',
                                          'Connection': 'keep-alive',
                                          'Referer': 'https://discord.com/',
                                          'Sec-Fetch-Dest': 'empty',
                                          'Sec-Fetch-Mode': 'cors',
                                          'Sec-Fetch-Site': 'same-origin'},
                                      json={'wp': wp, 's': s})
        if response.status_code == 200:
            return self._session.cookies.get("cf_clearance")
        else:
            return None


def main():
    client = CloudflareBypass()
    cf_ray = client.get_cookies()
    key, s = client.get_main_js()
    print(key, s)
    wp = client.calculate_wp(key)
    cf_clearance = client.get_cf_clearance(wp, s, cf_ray)
    print(cf_clearance)


if __name__ == '__main__':
    main()
