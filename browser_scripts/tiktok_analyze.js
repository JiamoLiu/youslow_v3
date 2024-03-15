var player = null
var currentURL = null
var interval = 1000
var sendData = {}
var extension_loaded_time = Date.now()
let intervalID = null;
let safeProperties = ['ATTRIBUTE_NODE','CDATA_SECTION_NODE','COMMENT_NODE','DOCUMENT_FRAGMENT_NODE','DOCUMENT_NODE','DOCUMENT_POSITION_CONTAINED_BY','DOCUMENT_POSITION_CONTAINS','DOCUMENT_POSITION_DISCONNECTED','DOCUMENT_POSITION_FOLLOWING','DOCUMENT_POSITION_IMPLEMENTATION_SPECIFIC','DOCUMENT_POSITION_PRECEDING','DOCUMENT_TYPE_NODE','ELEMENT_NODE','ENTITY_NODE','ENTITY_REFERENCE_NODE','HAVE_CURRENT_DATA','HAVE_ENOUGH_DATA','HAVE_FUTURE_DATA','HAVE_METADATA','HAVE_NOTHING','NETWORK_EMPTY','NETWORK_IDLE','NETWORK_LOADING','NETWORK_NO_SOURCE','NOTATION_NODE','PROCESSING_INSTRUCTION_NODE','TEXT_NODE','accessKey','attributeStyleMap','attributes','autocapitalize','autofocus','autoplay','baseURI','buffered','childElementCount','childNodes','children','classList','className','clientHeight','clientLeft','clientTop','clientWidth','contentEditable','controls','controlsList','crossOrigin','currentSrc','currentTime','dataset','defaultMuted','defaultPlaybackRate','dir','disablePictureInPicture','disableRemotePlayback','draggable','duration','elementTiming','ended','enterKeyHint','height','hidden','id','inert','innerHTML','innerText','inputMode','isConnected','isContentEditable','lang','localName','loop','muted','namespaceURI','networkState','nonce','offsetHeight','offsetLeft','offsetParent','offsetTop','offsetWidth','outerHTML','outerText','ownerDocument','parentElement','parentNode','part','paused','playbackRate','played','playsInline','poster','preload','preservesPitch','readyState','remote','scrollHeight','scrollLeft','scrollTop','scrollWidth','seekable','seeking','sinkId','slot','spellcheck','src','style','tabIndex','tagName','textContent','textTracks','title','translate','videoHeight','videoWidth','virtualKeyboardPolicy','volume','webkitAudioDecodedByteCount','webkitDecodedFrameCount','webkitDisplayingFullscreen','webkitDroppedFrameCount','webkitSupportsFullscreen','webkitVideoDecodedByteCount']

// Function to update sendData
function updateSendData() {
    const video = document.getElementsByTagName("video");
    if (video) {
        sendData.attributes = video[0].attributes;
        // sendData.autocapitalize = video[0].autocapitalize;
        // sendData.autofocus = video[0].autofocus;
        // sendData.autoplay = video[0].autoplay;
        // sendData.baseURI = video[0].baseURI;
        // sendData.buffered = video[0].buffered;
        // sendData.contentEditable = video[0].contentEditable;
        // sendData.controls = video[0].controls;
        // sendData.controlsList = video[0].controlsList;
        // sendData.crossOrigin = video[0].crossOrigin;
        // sendData.currentSrc = video[0].currentSrc;
        sendData.currentTime = video[0].currentTime;
        // sendData.defaultMuted = video[0].defaultMuted;
        // sendData.defaultPlaybackRate = video[0].defaultPlaybackRate;
        // sendData.disablePictureInPicture = video[0].disablePictureInPicture;
        // sendData.disableRemotePlayback = video[0].disableRemotePlayback;
        // sendData.draggable = video[0].draggable;
        sendData.duration = video[0].duration;
        // sendData.ended = video[0].ended;
        sendData.extension_loaded_time = extension_loaded_time
        sendData.isConnected = video[0].isConnected;
        // sendData.isContentEditable = video[0].isContentEditable;
        // sendData.localName = video[0].localName;
        // sendData.loop = video[0].loop;
        // sendData.muted = video[0].muted;
        // sendData.namespaceURI = video[0].namespaceURI;
        sendData.networkState = video[0].networkState;
        // sendData.outerHTML = video[0].outerHTML;
        // sendData.outerText = video[0].outerText;
        // sendData.ownerDocument = video[0].ownerDocument;
        // sendData.parentElement = video[0].parentElement;
        // sendData.parentNode = video[0].parentNode;
        sendData.paused = video[0].paused;
        sendData.platform = "tiktok"
        sendData.playbackRate = video[0].playbackRate;
        // sendData.played = video[0].played;
        // sendData.playsInline = video[0].playsInline;
        sendData.preload = video[0].preload;
        // sendData.preservesPitch = video[0].preservesPitch;
        sendData.readyState = video[0].readyState;
        sendData.remote = video[0].remote;
        // sendData.src = video[0].src;
        // sendData.translate = video[0].translate;
        sendData.url = window.location.href
        sendData.videoHeight = video[0].videoHeight;
        sendData.videoWidth = video[0].videoWidth
        sendData.webkitAudioDecodedByteCount = video[0].webkitAudioDecodedByteCount
        sendData.webkitDecodedFrameCount = video[0].webkitDecodedFrameCount
        // sendData.webkitDisplayingFullscreen = video[0].webkitDisplayingFullscreen
        sendData.webkitDroppedFrameCount = video[0].webkitDroppedFrameCount
        // sendData.webkitSupportsFullscreen = video[0].webkitSupportsFullscreen
        sendData.webkitVideoDecodedByteCount = video[0].webkitVideoDecodedByteCount
    }
}
updateSendData();
return sendData;
