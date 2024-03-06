var name = document.getElementById('name').innerHTML
var SCHEMA = parseInt(document.getElementById('SCHEMA').innerHTML)
console.log(name, SCHEMA)

var ansString = document.getElementById('ansString').innerHTML
console.log(ansString);
var ansOBJ = JSON.parse(ansString)
console.log('ansOBJ', ansOBJ);

var report = navigator.userAgent
console.log(report);
var device = null
var notice = null
var desktop = false



if (report.includes('Windows')){
  device = 'A'
  desktop = true
  notice = 'Recording in Windows'
}
else if (report.includes('Line')){
    device = 'L'
    notice = 'WARNING - LINE APP cannot be used for recording'
}
else if (report.includes('FB')){
    device = 'FB'
    notice = 'WARNING - FACEBOOK APP cannot be used for recording'
}
else if (report.includes('Android')){
    device = 'A'
    notice = 'Recording in Android'
}
else if (report.includes('Macintosh')){
    device = 'I'
    notice = 'Recording on Mac, recording may not work on this computer'
}
else if (report.includes('iPad')){
    notice = 'Recording on iPad may not work; please upload file or use a phone/computer'
    device = 'I'
}
else if (report.includes('iPhone OS')){
  console.log('Found iPhone OS')
  for (var n = 0; n < 30; n++) {
    if (n >= 10 && report.includes('iPhone OS ' + n)) {
      device = 'I'
      notice = 'Recording in iOS ' + n
      break
    } else {
      device = 'I'
      notice = 'Recording in iOS <10'
    }
  }
}
else {
  device = 'U'
  notice = 'Your OS may not work; if so try upload a file, share a link, or use a computer; ' + report
}
console.log('DEVICE', device);


if (name == 'Test'){
  alert('Hi Test, this is a test:  ' + device +'__'+ notice )
}

//iphone recording
window.globalFunc = function (action){
  console.log('global started');
  window.URL = window.URL || window.webkitURL;
  /**
   * Detect the correct AudioContext for the browser
   * */
  window.AudioContext = window.AudioContext || window.webkitAudioContext;
  navigator.getUserMedia  = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
  var recorder = new RecordVoiceAudios();


  if (action == 'start'){
    recorder.startRecord()
    console.log('recorder start');
  }
  else if (action == 'stop'){
    recorder.stopRecord();
  }

  function RecordVoiceAudios() {

      let encoder = null;
      let microphone;

      var audioContext;
      let processor;
      let config = {
          bufferLen: 4096,
          numChannels: 2,
          mimeType: 'audio/mpeg'
      };
      console.log('load rec voice');

      this.startRecord = function() {
        console.log('startRecord');
          audioContext = new AudioContext();
          /** Create a ScriptProcessorNode with a bufferSize of
          * 4096 and two input and output channel
          * */
          if (audioContext.createJavaScriptNode) {
              processor = audioContext.createJavaScriptNode(config.bufferLen, config.numChannels, config.numChannels);
              console.log('java processer');
          } else if (audioContext.createScriptProcessor) {
              processor = audioContext.createScriptProcessor(config.bufferLen, config.numChannels, config.numChannels);
              console.log('script processer');
          } else {
              console.log('WebAudio API has no support on this browser.');
          }
          processor.connect(audioContext.destination);
          /**
          *  ask permission of the user for use microphone or camera
          * */
          navigator.mediaDevices.getUserMedia({ audio: true, video: true })
          .then(gotStreamMethod)
          .catch('logError');
      };

      let getBuffers = (event) => {
          var buffers = [];
          for (var ch = 0; ch < 2; ++ch)
              buffers[ch] = event.inputBuffer.getChannelData(ch);
          return buffers;
      }

      let gotStreamMethod = (stream) => {

          config = {
              bufferLen: 4096,
              numChannels: 2,
              mimeType: 'audio/mpeg'
          };

          let tracks = stream.getTracks();
          /**Create a MediaStreamAudioSourceNode for the microphone **/
          microphone = audioContext.createMediaStreamSource(stream);
          /**connect the AudioBufferSourceNode to the gainNode **/
          microphone.connect(processor);
          encoder = new Mp3LameEncoder(audioContext.sampleRate, 160); //bitRate set to 160
          /** Give the node a function to process audio events **/
          processor.onaudioprocess = function(event) {
              encoder.encode(getBuffers(event));
              console.log('MP3 encoding');
          };

          stopBtnRecord = () => {
                  var stage = 1
                  console.log('stop Record');
                  audioContext.close();
                  processor.disconnect();
                  tracks.forEach(track => track.stop());
                  stage = 2
                  audioElement = document.getElementById('handler')
                  audioElement.src = URL.createObjectURL(encoder.finish());
                  stage = 3

                  globlob = audioElement.src

                    fetch(audioElement.src)
                    .then( response => response.blob() )
                    .then( blob =>{
                        var reader = new FileReader();
                        reader.readAsDataURL(blob);
                        reader.onload = function(){
                            var base64data = this.result.split(',')[1]  // <-- this.result contains a base64 data URI
                            b64d = base64data
                        }; //end reader.onload

                    })//end fetch then
                    .catch((error) => {
                      console.log(error);
                      recErrorWin(error);
                    })
                  return stage

          };// stopRecord
      }
      this.stopRecord = function() {
        try{
          var stage = stopBtnRecord()
          console.log(stage);
        }
        catch {
          recErrorWin('Apple fail before fetch');
        }

      };
  }
}


function recErrorWin (message){

  $.ajax({
    data : {
        unit : 'A',
        message : message,
        mode : notice
    },
    type : 'POST',
    url : '/recError'
    })
    .done(function(data) {
      alert('error has occured - your device is unable to record - please try to upload mp3 instead - sorry for the inconvenience')
    })
    .fail(function(){
      alert('error has occured - your device is unable to record - please try to upload mp3 instead - sorry for the inconvenience')
    });

}

//device = 'U'
let b64d = 'nothing'
let globlob = 'noURL'


startVue(ansOBJ, device)

function startVue(ansOBJ, device){

  let vue = new Vue({

    el: '#vue-app',
    delimiters: ['[[', ']]'],
    mounted: function () {
      this.audioCheck()
      this.videoCheck()
      // this.textCheck()
    },
    data: {
        title: {
          1 : 'Pronunciation Model 1',
          2 : 'Pronunciation Model 2',
          3 : 'Pronunciation Model 3'
        },
        notice : notice,
        showVideo : false,
        showSpeak: {
          1 : true,
          2 : true,
          3 : true
        },
        showCapture: {
          1 : true,
          2 : true,
          3 : true
        },
        audio: {
          1 : null,
          2 : null,
          3 : null,
        },
        video: {
          1 : null,
          2 : null,
          3 : null,
        },
        text: {
          1 : ['',''],
          2 : ['',''],
          3 : ['','']
        },
        uploadBTN : {
          1 : ['upbtn1', 'uplink1'],
          2 : ['upbtn2', 'uplink2'],
          3 : ['upbtn3', 'uplink3']
        },
        ansOBJ: ansOBJ,
        device: device,
        rec1: {
            start : true,
            stop : false,
            save : false,
            cancel : false,
            timer : false,
            t_style: false,
            count : false
        },
        capture1: {
            play : true,
            capture : true,
            start : false,
            stop : false,
            save : false,
            cancel : false,
            timer : false,
            t_style: false,
            count : false
        },
        rec_timer : null,
        mediaRecorder : null,
        captureRecorder : null,
        audio_source : null,
        base64data : null,
        blobURL : null,
        upload : false,
        SCHEMA : SCHEMA,
        desktop : desktop,
        echoMessage : '',
        echoTimer : null,
        echoCount : '',
        echoBlock : null,
        dataChunks : []
    },
    methods: {
      start_speak: function (task) {
        vue.echoBlock = task
        console.log('start', task)
        this.echoMessage = 'LISTEN....'

        for (var key in vue.showSpeak){
          console.log(key, task, vue.showSpeak);
          if (key != task) {
            vue.showSpeak[key] = false
          }
        }
        for (var key in vue.showCapture){
          vue.showCapture[key] = false
        }

        this.playVideo(task, 'video')

        document.getElementById('handlerVideo').addEventListener('ended', function(e) {
            vue.echoMessage = 'ECHO...'
            vue.echoCount = 3
            vue.echoTimer = setInterval(function() {
              vue.echoCount -= 1
            }, 1000)

            setTimeout(function() {
              clearInterval(vue.echoTimer)
              vue.echoCount = ''
              vue.echoTimer = null
              vue.start(task)
            }, 3000)
        })
      },
      start : function(task){
        this.echoMessage = 'REPEAT...'

        vue.rec1.start = false
        vue.rec1.stop = true
        vue.rec1.timer = true

        vue.timer()

        if (this.device == 'A') {
        var constraintObj = {audio: true, video: false };
        navigator.mediaDevices.getUserMedia(constraintObj)
            .then(function(mediaStreamObj) {
                vue.mediaRecorder = new MediaRecorder(mediaStreamObj);
                var chunks = [];
                vue.mediaRecorder.start();
                console.log('status:' + vue.mediaRecorder.state);

              vue.mediaRecorder.ondataavailable = function(ev) {
                chunks.push(ev.data);
              }

              vue.mediaRecorder.onstop = (ev)=>{
                    try{
                      var blob = new Blob(chunks, { type : 'audio/webm' });
                      console.log(blob);
                      chunks = [];// here we clean out the array
                      var blobURL = window.URL.createObjectURL(blob);
                      console.log(blobURL);
                      //get the base64data string from the blob
                      reader = new FileReader();
                      reader.readAsDataURL(blob);
                      reader.onloadend = function() {
                        vue.base64data = reader.result.split(',')[1]; //remove padding from beginning of string
                        vue.blobURL = blobURL
                      }
                    }
                    catch(err) {
                      console.log(err.message);
                      vue.recError(err.message)
                    }
                }
             })
          }
          else if (this.device == 'I'){
            // global function for iphone recording
            window.globalFunc('start')
          }
      },
      stop: function(task){
        this.echoMessage = 'CHECK...'
        vue.rec1.stop = false
        vue.rec1.save = true
        vue.rec1.cancel = true
        clearInterval(vue.rec_timer)
        console.log(this.device);

            if (this.device == 'A') {
              console.log('stopped');
              vue.audio[task] = 3
              vue.mediaRecorder.stop();
              console.log('status:' + vue.mediaRecorder.state);
            }
            else if (this.device == 'I'){
              // global function for iphone recording
              vue.audio[task] = 3
              window.globalFunc('stop')
              vue.blobURL = globlob
              console.log('status: mp3 rec stopped');
            }


      },
      cancel: function(){
        vue.echoBlock = null
        this.echoMessage = ''
        clearInterval(vue.rec_timer)
        console.log('cancel');
        for (var key in vue.rec1){
          vue.rec1[key] = false
        }
        vue.rec1.start = true


        for (var key in vue.showCapture){
          vue.showCapture[key] = true
        }
        for (var key in vue.showSpeak){
          vue.showSpeak[key] = true
        }
        vue.base64data = null
        vue.blobURL = null
        this.audioCheck()
      },
      setup_capture : function(task){
        if (!this.desktop) {
          alert('Cannot screen capture on mobile device, please use a computer')
          return false
        }
        vue.echoBlock = task
        console.log('setup capture', task)

        for (var key in vue.showCapture){
          if (key != task) {
            vue.showCapture[key] = false
          }
        }
        for (var key in vue.showSpeak){
          vue.showSpeak[key] = false
        }

        vue.capture1.capture = false
        vue.capture1.play = false
        vue.capture1.start = true
        // vue.capture1.timer = true
        // vue.timer_capture()
        vue.chunks = []

        var constraintObj = {audio: true, video: true};
        navigator.mediaDevices.getDisplayMedia(constraintObj)
            .then(function(mediaStreamObj) {
                vue.captureRecorder = new MediaRecorder(mediaStreamObj);

              vue.captureRecorder.ondataavailable = function(ev) {
                vue.chunks.push(ev.data);
              }

              // vue.captureRecorder.oninactive = function(ev) {
              //   console.log('inactive', task, ev)
              //   vue.stop_capture(task)
              // }

              vue.captureRecorder.onstop = (ev)=>{
                    try{
                      /// screen capture
                      var blob = new Blob(vue.chunks, { type : 'video/webm' });
                      console.log(blob);
                      vue.chunks = [];// here we clean out the array
                      var blobURL = window.URL.createObjectURL(blob);
                      console.log(blobURL);
                      //get the base64data string from the blob
                      reader = new FileReader();
                      reader.readAsDataURL(blob);
                      reader.onloadend = function() {
                        vue.base64data = reader.result.split(',')[1]; //remove padding from beginning of string
                        vue.blobURL = blobURL
                      }
                    }
                    catch(err) {
                      console.log(err.message);
                      vue.recError(err.message)
                    }
                }
             })

      },
      start_capture : function(task){
        if (!this.desktop) {
          alert('Cannot screen capture on mobile device, please use a computer')
          return false
        }
        console.log('start capture', task)

        for (var key in vue.showCapture){
          if (key != task) {
            vue.showCapture[key] = false
          }
        }
        for (var key in vue.showSpeak){
          vue.showSpeak[key] = false
        }

        vue.capture1.start = false
        vue.capture1.stop = true
        vue.capture1.timer = true
        vue.timer_capture()
        vue.captureRecorder.start()

      },
      stop_capture : function(task){

        vue.capture1.stop = false
        vue.capture1.play = true
        vue.capture1.save = true
        vue.capture1.cancel = true
        clearInterval(vue.rec_timer)
        console.log(this.device);

        console.log('stopped');
        vue.video[task] = 3
        vue.captureRecorder.stop();
        console.log('capture status:' + vue.captureRecorder.state);
      },
      cancel_capture: function(){
        clearInterval(vue.rec_timer)
        console.log('cancel');
        for (var key in vue.capture1){
        vue.capture1[key] = false
        }
        vue.capture1.capture = true
        vue.capture1.play = true

        for (var key in vue.showCapture){
          vue.showCapture[key] = true
        }
        for (var key in vue.showSpeak){
          vue.showSpeak[key] = true
        }
        vue.base64data = null
        vue.blobURL = null
        this.videoCheck()
      },
      recError : function (message){

        $.ajax({
          data : {
              unit : vue.ansOBJ.Unit,
              message : message,
              mode : notice
          },
          type : 'POST',
          url : '/recError'
          })
          .done(function(data) {
            alert('error has occured - your device is unable to record - please contact your instructor')
          })
          .fail(function(){
            alert('error has occured - your device is unable to record - please contact your instructor')
          });
          console.log(vue.ansOBJ);
      },
      save : function (task, mark){
        if (this.device == 'I'){
          vue.base64data = b64d
        }


        vue.ansOBJ[task]['Length'] = vue.rec1.count
        file_title = (vue.ansOBJ.Unit + '_' + task + '_' + device)

        $.ajax({
          data : {
              type : 'record',
              task : task,
              unit : vue.ansOBJ.Unit,
              title : file_title,
              base64 : vue.base64data,
              ansDict : JSON.stringify(vue.ansOBJ)
          },
          type : 'POST',
          url : '/pr_audioUpload'
          })
          .done(function(data) {

              vue.cancel()
              if (data.grade == 0){
                alert('Speaking Upload successful\r\nKeep going')
              }
              else if (data.grade == 1){
                alert('Assignment complete\r\nLate submission\r\n1 point\r\nGo back to assignments')
              }
              else if (data.grade == 2){
                alert('Assignment completed on time\r\n 2 points\r\nGo back to assignments')
              }
              location.reload()
          })
          .fail(function(){
            alert('Upload Failed, there has been an error. Reload the page and if it happens again please tell you instructor')
          });
          console.log(vue.ansOBJ);
      },
      save_capture : function (task, mark){

        vue.ansOBJ[task]['Length'] = vue.capture1.count
        file_title = (vue.ansOBJ.Unit + '_' + task + '_capture')

        $.ajax({
          data : {
              type : 'capture',
              task : task,
              unit : vue.ansOBJ.Unit,
              title : file_title,
              base64 : vue.base64data,
              ansDict : JSON.stringify(vue.ansOBJ)
          },
          type : 'POST',
          url : '/pr_audioUpload'
          })
          .done(function(data) {

              vue.cancel()
              if (data.grade == 0){
                alert('Capture Upload successful\r\nKeep going')
              }
              else if (data.grade == 1){
                alert('Assignment complete\r\nLate submission\r\n1 point\r\nGo back to assignments')
              }
              else if (data.grade == 2){
                alert('Assignment completed on time\r\n 2 points\r\nGo back to assignments')
              }
              location.reload()
          })
          .fail(function(){
            alert('Upload Failed, there has been an error. Reload the page and if it happens again please tell you instructor')
          });
          console.log(vue.ansOBJ);
      },
      textCheck : function(){
        if (this.ansOBJ['1']['TextData'][0] == '' || this.ansOBJ['1']['TextData'][1] == ''){
          this.showCapture['1'] = false
          this.showSpeak['1'] = false
        }
        if (this.ansOBJ['2']['TextData'][0] == '' || this.ansOBJ['2']['TextData'][1] == ''){
          this.showCapture['2'] = false
          this.showSpeak['2'] = false
        }
        if (this.ansOBJ['3']['TextData'][0] == '' || this.ansOBJ['3']['TextData'][1] == ''){
          this.showCapture['3'] = false
          this.showSpeak['3'] = false
        }
        if (this.ansOBJ['1']['VideoData'] == null){
          this.showSpeak['1'] = false
        }
        if (this.ansOBJ['2']['VideoData'] == null){
          this.showSpeak['2'] = false
        }
        if (this.ansOBJ['3']['VideoData'] == null){
          this.showSpeak['3'] = false
        }
      },
      checkShow: function (key, show) {
        //console.log(key, show, this.showCapture[key])
        if (show == 'capture') {
          if (this.ansOBJ[key]['TextData'][0] == '' || this.ansOBJ[key]['TextData'][1] == ''){
            // this.showCapture[key] = false
            // this.showSpeak[key] = false
            return false
          } else {
            return this.showCapture[key]
          }
        } else {
          if (this.ansOBJ[key]['VideoData'] == null){
            // this.showSpeak[key] = false
            return false
          } else {
            return this.showSpeak[key]
          }
        }
      },
      audioCheck : function(){
        if (this.ansOBJ['1']['AudioData'] == null){
          this.audio['1'] = 1
        }
        else{
          this.audio['1'] = 2
        }
        if (this.ansOBJ['2']['AudioData'] == null){
          this.audio['2'] = 1
        }
        else{
          this.audio['2'] = 2
        }
        if (this.ansOBJ['3']['AudioData'] == null){
          this.audio['3'] = 1
        }
        else{
          this.audio['3'] = 2
        }
      },
      videoCheck : function(){
        if (this.ansOBJ['1']['VideoData'] == null){
          this.video['1'] = 1
        }
        else{
          this.video['1'] = 2
        }
        if (this.ansOBJ['2']['VideoData'] == null){
          this.video['2'] = 1
        }
        else{
          this.video['2'] = 2
        }
        if (this.ansOBJ['3']['VideoData'] == null){
          this.video['3'] = 1
        }
        else{
          this.video['3'] = 2
        }
      },
      timer : function (task){
        vue.rec_timer = setInterval(function() {
            if (vue.rec1.count) {
              console.log(vue.rec1.count);
            }
            else{
              vue.rec1.count = 0
            }

            vue.rec1.count += 1
            if (vue.rec1.count == 121){
                vue.stop(task)
                console.log('timer_terminated');
            }
            else {
                var width =  vue.rec1.count + '%'
                var color = 'indianred'
                if (vue.rec1.count > 80){
                  color = 'red'
                }
                else if (vue.rec1.count > 30){
                  color = 'mediumseagreen'
                }
                else if (vue.rec1.count > 20) {
                  color = 'khaki'
                }
                else if (vue.rec1.count > 10) {
                  color = 'coral'
                }
                vue.rec1.t_style = { height:'30px', width:width, background:color, color:'white', 'border-radius': '5px', border: '1px solid white' }
            }
          }, 1000)
      },
      timer_capture : function (task){
        vue.rec_timer = setInterval(function() {
            if (vue.capture1.count) {
              console.log(vue.capture1.count);
            }
            else{
              vue.capture1.count = 0
            }

            vue.capture1.count += 1
            if (vue.capture1.count == 121){
                vue.stop(task)
                console.log('timer_terminated');
            }
            else {
                var width =  vue.capture1.count + '%'
                var color = 'indianred'
                if (vue.capture1.count > 80){
                  color = 'red'
                }
                else if (vue.capture1.count > 30){
                  color = 'mediumseagreen'
                }
                else if (vue.capture1.count > 20) {
                  color = 'khaki'
                }
                else if (vue.capture1.count > 10) {
                  color = 'coral'
                }
                vue.capture1.t_style = { height:'30px', width:width, background:color, color:'white', 'border-radius': '5px', border: '1px solid white' }
            }
          }, 1000)
      },
      playAudio : function (arg) {

        let playlist = {
          '0' : vue.blobURL,
          '1' : vue.ansOBJ['1']['AudioData'],
          '2' : vue.ansOBJ['2']['AudioData'],
          '3' : vue.ansOBJ['3']['AudioData'],
        }
        console.log(playlist[arg])
        player = document.getElementById('handler')

        player.src = playlist[arg]

      },
      playVideo: function (arg, mode) {
        vue.echoBlock = arg

        let playlist = {
          '0' : vue.blobURL,
          '1' : vue.ansOBJ['1']['VideoData'],
          '2' : vue.ansOBJ['2']['VideoData'],
          '3' : vue.ansOBJ['3']['VideoData'],
        }
        if (mode == 'video') {
          this.showVideo = true
          player = document.getElementById('handlerVideo')
        } else {
          player = document.getElementById('handler')
        }
        console.log(playlist[arg], player)
        player.src = playlist[arg]

      },
      stop_video: function () {
        vue.echoBlock = null
        this.showVideo = false
        player = document.getElementById('handlerVideo')
        player.src = null
      },
      videoDisplay: function () {
        if (!this.showVideo) {
          return 'display:none'
        }
      },
      fileValidation : function(task){
        var fileInput = document.getElementById('upbtn'+ task);
        console.log('file', fileInput)
        var filePath = fileInput.value;
        var allowedExtensions = /(\.mp3|\.m4a|\.m4v|\.mov|\.mp4|\.aac)$/i;

        if(fileInput.files[0].size > 88000000){
            alert("File is too big!");
            location.reload()
            return false;
        }
        else if(!allowedExtensions.exec(filePath)){
            alert('Please upload audio file: .mp3/.m4a only.');
            fileInput.value = '';
            return false;
        }
        else{
            console.dir( fileInput.files[0] );
            var url = window.URL.createObjectURL(fileInput.files[0]);
            fetch(url)
            .then(function(res){
                return res.blob();
                })
            .then(function(savedBlob){

            var seconds = new Promise ((resolve,reject) =>{
                var savedBlobURL = window.URL.createObjectURL(savedBlob);
                let audio = document.getElementById('handler');
                audio.src = savedBlobURL;
                audio.addEventListener('loadedmetadata', function() {
                    var audioLen = Math.round(audio.duration);
                    vue.rec1.count = audioLen
                    console.log('seconds uploaded: ' + vue.rec1.count)
                    })
                setTimeout(func, 1000)
                function func(){ resolve ('length complete for task' + task)}
            })

            var base = new Promise ((resolve,reject) =>{
                var reader = new FileReader();
                reader.readAsDataURL(savedBlob);
                reader.onloadend = function() {
                    vue.base64data = reader.result.split(',')[1];
                    }
                setTimeout(func, 1000)
                function func(){ resolve ('base64 complete for task ' + task)}
            })

            Promise.all([ seconds, base ])
            .then((messages) => {
                console.log(messages)
                alert ('Your assignment will be updated, please wait')
                vue.save(task)
                })
            })
        }//end else
      },//end fileValidation
      saveLink : function(task){
          vue.base64data = document.getElementById('uplink' + task).value
          vue.rec1.count = 1
          console.log( 'link stored for task ' + task)
          this.save(task, 'link')
      }
    } // end methods



  })// end NEW VUE

}// endFunction



