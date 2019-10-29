var constraints = window.constraints = {
    audio: false,
    video: {
        width: {
            exact: 640
        }, 
        height: {
            exact: 480
        },
        framerate: 20
    }
}

var videoTracks;
const video = document.querySelector('video');
const canvas = window.canvas = document.querySelector('canvas');
canvas.width = 640;
canvas.height = 480;

let mediaRecorder;
let recordedBlobs;
let sourceBuffer;

var linkImage = "";
var linkRecord = "";
// const mainLink = "/Users/macintoshhd/Desktop/code/face-fix/public/"
const mainLink = "/home/pi/face/face/public/"
function sendLinkImage(){
    console.log(mainLink + "img/" + linkImage + ".png");
    socket.emit("image",{
        "source":"MainApp",
        "func":"recognize",
        "data":{
            "base64image": mainLink + "img/" + linkImage + ".png"
        }}
    )
}

var id_ = 0;
function sendLinkRecord(name){
    socket.emit("record", {
        "source":"MainApp",
        "func":"register",
        "data":{
            "username":name,
            "ID": id_,
            "base64video":mainLink + "record/" + linkRecord + ".webm",
            "base64image":mainLink + "img/" + linkImage + ".png",
            "isportrait": false,
            "overwrite": true
        }}
    )
}

function processPhoto(blob){
    var fd = new FormData();

    linkImage = "image" + "_" + (new Date()).getTime();
    console.log("NAME IMAGE:", linkImage);
    fd.append("fname", linkImage);    
    fd.append("data", blob);
    jQuery.ajax({
        type: 'POST', 
        url: "/upload/image", 
        data: fd, 
        processData: false, 
        contentType: false
        
    }).done(function(data){
        sendLinkImage();
        console.log(data);
    }); 
}

function uploadImage() {
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    let captureDevice = new ImageCapture(videoTracks[0]);
    if (captureDevice) {
        captureDevice.takePhoto().then(processPhoto).catch(stopCamera);
    }  
};

function stopCamera(error) {
    console.error(error);
    // if (videoDevice) videoDevice.stop();  // turn off the camera
  }

function uploadRecord(name){
    const blob = new Blob(recordedBlobs, {type: 'video/webm'});
    var fd = new FormData();
    linkRecord = "video" + "_" + (new Date()).getTime();
    fd.append("fname", linkRecord);
    fd.append("data", blob);
    jQuery.ajax({
        type: 'POST', 
        url: "/upload/record", 
        data: fd, 
        processData: false, 
        contentType: false
    }).done(function(data){

        sendLinkRecord(name);
        console.log(data)
    });
}

function handleDataAvailable(event) {
    if (event.data && event.data.size > 0) {
      recordedBlobs.push(event.data);
    }
}

function stopRecording() {
    mediaRecorder.stop();
    console.log('Recorded Blobs: ', recordedBlobs);
}

function startRecording() {
    recordedBlobs = [];
    let options = {mimeType: 'video/webm;codecs=vp9'};
    if (!MediaRecorder.isTypeSupported(options.mimeType)) {
        console.error(`${options.mimeType} is not Supported`);
        errorMsgElement.innerHTML = `${options.mimeType} is not Supported`;
        options = {mimeType: 'video/webm;codecs=vp8'};
        if (!MediaRecorder.isTypeSupported(options.mimeType)) {
            console.error(`${options.mimeType} is not Supported`);
            errorMsgElement.innerHTML = `${options.mimeType} is not Supported`;
            options = {mimeType: 'video/webm'};
            if (!MediaRecorder.isTypeSupported(options.mimeType)) {
                console.error(`${options.mimeType} is not Supported`);
                errorMsgElement.innerHTML = `${options.mimeType} is not Supported`;
                options = {mimeType: ''};
            }
        }
    }
  
    try {
        mediaRecorder = new MediaRecorder(window.stream, options);
    } catch (e) {
        console.error('Exception while creating MediaRecorder:', e);
        errorMsgElement.innerHTML = `Exception while creating MediaRecorder: ${JSON.stringify(e)}`;
        return;
    }
  
    console.log('Created MediaRecorder', mediaRecorder, 'with options', options);
    // recordButton.textContent = 'Stop Recording';
    // playButton.disabled = true;
    // downloadButton.disabled = true;
    mediaRecorder.onstop = (event) => {
      console.log('Recorder stopped: ', event);
    };
    mediaRecorder.ondataavailable = handleDataAvailable;
    mediaRecorder.start(10); // collect 10ms of data
    console.log('MediaRecorder started', mediaRecorder);
}

function handleSuccess(stream) {
    /* DISPLAY CAMERA IN VIDEO */
    // const video = document.querySelector('video');
    videoTracks = stream.getVideoTracks();
    console.log('Got stream with constraints:', constraints);
    console.log(`Using video device: ${videoTracks[0].label}`);
    window.stream = stream; // make variable available to browser console
    video.srcObject = stream;
}
  
function handleError(error) {
    if (error.name === 'ConstraintNotSatisfiedError') {
        let v = constraints.video;
        errorMsg(`The resolution ${v.width.exact}x${v.height.exact} px is not supported by your device.`);
    } else if (error.name === 'PermissionDeniedError') {
        errorMsg('Permissions have not been granted to use your camera and ' +
        'microphone, you need to allow the page access to your devices in ' +
        'order for the demo to work.');
    }
    errorMsg(`getUserMedia error: ${error.name}`, error);
}
  
function errorMsg(msg, error) {
    const errorElement = document.querySelector('#errorMsg');
    errorElement.innerHTML += `<p>${msg}</p>`;
    if (typeof error !== 'undefined') {
        console.error(error);
    }
}

async function init() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        handleSuccess(stream);
        // e.target.disabled = true;
    } catch (e) {
        handleError(e);
    }
}

init();