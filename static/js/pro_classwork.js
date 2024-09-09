var ansString = document.getElementById('ansDict').innerHTML

// var ansOBJ = JSON.parse(ansString)
var ansOBJsnl = {
    "1": {
        "question": "---",
        "answer1": "tack",
        "answer2": "tech",
        "user": "Haoyuchan",
        "audioLink": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/02/2/1_4906_audioLink.mp3",
        "imageLink": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/02/2/1_3403_imageLink.jpg",
        "imageLink2": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/02/2/1_3414_imageLink2.jpg"
    },
    "2": {
        "question": "---",
        "answer1": "axe",
        "answer2": "ex",
        "user": "Haoyuchan",
        "audioLink": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/02/2/2_4958_audioLink.mp3",
        "imageLink": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/02/2/2_3536_imageLink.jpg",
        "imageLink2": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/02/2/2_3547_imageLink2.jpg"
    },
    "3": {
        "question": "---",
        "answer1": "bag",
        "answer2": "beg",
        "user": "Nina Chen",
        "audioLink": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/02/2/3_0459_audioLink.mp3",
        "imageLink": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/02/2/3_5211_imageLink.jpg",
        "imageLink2": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/02/2/3_5301_imageLink2.jpg"
    },
    "4": {
        "question": "---",
        "answer1": "cup",
        "answer2": "cop",
        "user": "Nina Chen",
        "audioLink": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/02/2/4_0705_audioLink.mp3",
        "imageLink": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/02/2/4_5835_imageLink.jpg",
        "imageLink2": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/02/2/4_0804_imageLink2.jpg"
    },
    "5": {
        "question": "---",
        "answer1": "caught",
        "answer2": "cut",
        "user": "Nora",
        "audioLink": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/02/2/5_4457_audioLink.mp3",
        "imageLink": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/02/2/5_4941_imageLink.jpg",
        "imageLink2": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/02/2/5_4137_imageLink2.jpg"
    },
    "6": {
        "question": "---",
        "answer1": "boss",
        "answer2": "bus",
        "user": "Nora",
        "audioLink": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/02/2/6_5955_audioLink.mp3",
        "imageLink": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/02/2/6_4919_imageLink.jpg",
        "imageLink2": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/02/2/6_4855_imageLink2.png"
    }
}

var ansOBJ = {
    "1": {
        "question": "Could you cut the _______ off the pizza, Please?",
        "answer1": "Crust",
        "answer2": "Crossed",
        "user": "Haoyuchan",
        "audioLink": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/02/2/1_4726_audioLink.mp3",
        "imageLink": "----",
        "imageLink2": "----"
    },
    "2": {
        "question": "A ___ lay under the table, gnawing on a bone.",
        "answer1": "dog",
        "answer2": "dug",
        "user": "Nina Chen",
        "audioLink": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/02/2/2_2648_audioLink.mp3",
        "imageLink": "----",
        "imageLink2": "----"
    },
    "3": {
        "question": "The party is not ____  yet.",
        "answer1": "Done",
        "answer2": "Dawn",
        "user": "Haoyuchan",
        "audioLink": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/02/2/3_4817_audioLink.mp3",
        "imageLink": "----",
        "imageLink2": "----"
    },
    "4": {
        "question": "Does she remember to bring her ____________ ?",
        "answer1": "axe",
        "answer2": "ex",
        "user": "Nora",
        "audioLink": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/02/2/4_1936_audioLink.mp3",
        "imageLink": "----",
        "imageLink2": "----"
    },
    "5": {
        "question": "She looked through all the drawers, looking for a _____.",
        "answer1": "pen",
        "answer2": "pan",
        "user": "Nina Chen",
        "audioLink": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/02/2/5_3143_audioLink.mp3",
        "imageLink": "----",
        "imageLink2": "----"
    },
    "6": {
        "question": "What are the benefits of owning a ________ ?",
        "answer1": "kettle",
        "answer2": "cattle",
        "user": "Nora",
        "audioLink": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/02/2/6_5403_audioLink.mp3",
        "imageLink": "----",
        "imageLink2": "----"
    }
}

console.log('ansOBJ', ansOBJ);

// ablank obj version of ansstring
var testString = document.getElementById('testDict').innerHTML
// var testOBJ = JSON.parse(testString)
var testOBJ = {
    "1": {
        "question": null,
        "answer1": null,
        "answer2": null,
        "user": null,
        "audioLink": null,
        "imageLink": "-----",
        "imageLink2": "-----"
    },
    "2": {
        "question": null,
        "answer1": null,
        "answer2": null,
        "user": null,
        "audioLink": null,
        "imageLink": "-----",
        "imageLink2": "-----"
    },
    "3": {
        "question": null,
        "answer1": null,
        "answer2": null,
        "user": null,
        "audioLink": null,
        "imageLink": "-----",
        "imageLink2": "-----"
    },
    "4": {
        "question": null,
        "answer1": null,
        "answer2": null,
        "user": null,
        "audioLink": null,
        "imageLink": "-----",
        "imageLink2": "-----"
    },
    "5": {
        "question": null,
        "answer1": null,
        "answer2": null,
        "user": null,
        "audioLink": null,
        "imageLink": "-----",
        "imageLink2": "-----"
    },
    "6": {
        "question": null,
        "answer1": null,
        "answer2": null,
        "user": null,
        "audioLink": null,
        "imageLink": "-----",
        "imageLink2": "-----"
    }
}
console.log('testOBJ', testOBJ);

var teamMembers = document.getElementById('teamMembers').innerHTML
// var teamOBJ = JSON.parse(teamMembers)
var teamOBJ = {
    "Nora": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/profiles/default.PNG",
    "Nina Chen": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/profiles/default.PNG",
    "Haoyuchan": "https://pron-lms.s3.ap-northeast-1.amazonaws.com/profiles/default.PNG"
}
console.log('teamOBJ', teamOBJ);

const mode = (window.location.href).split('/pro/')[1].split('/')[0]

if (mode == 'snl') {
    ansOBJ = ansOBJsnl
}
const unit = (window.location.href).split('/pro/')[1].split('/')[1]
const team = (window.location.href).split('/pro/')[1].split('/')[2]
console.log(mode, unit, team);

var name = document.getElementById('name').innerHTML


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
          console.log('Apple fail before fetch');
        }

      };
  }
}

//device = 'U'
let b64d = 'nothing'
let globlob = 'noURL'

startVue()

function startVue(){

  let vue = new Vue({

    el: '#vue-app',
    delimiters: ['[[', ']]'],
    mounted: function () {

        setInterval(function(){
            vue.updateAnswers()
        }, 15000)
        setTimeout(function(){
           vue.checkMarkers2()
        }, 2000);

    },
    data: {
        notice : notice,
        ansOBJ: ansOBJ,
        teamOBJ: teamOBJ,
        testOBJ: testOBJ,
        mode: mode,
        unit: unit,
        team: team,
        marker:{
            1 : 1,
            2 : 1,
            3 : 1,
            4 : 1,
            5 : 1,
            6 : 1,
        },
        buttonColor:{
            3 : {background: 'dodgerblue', padding: '5px'},
            2 : {background: 'mediumseagreen', padding: '5px'},
            1 : {background: 'lightcoral', padding: '5px'},
            0 : {background: 'silver', padding: '5px'}
        },
        image64 : {
            fileType : null,
            fileType2 : null,
            base64 : null,
        },

        audio64 : {
            fileType : null,
            base64 : null,
        },
        audio: {
            1 : null,
            2 : null,
            3 : null,
            4 : null,
            5 : null,
            6 : null,
        },
        uploadBTN : {
            1 : ['upbtn1', 'uplink1'],
            2 : ['upbtn2', 'uplink2'],
            3 : ['upbtn3', 'uplink3'],
            4 : ['upbtn1', 'uplink1'],
            5 : ['upbtn2', 'uplink2'],
            6 : ['upbtn3', 'uplink3'],
        },
        rec1: {
            start : true,
            stop : false,
            save : false,
            cancel : false,
            timer : false,
            t_style: false,
            count : false
        },
        rec_timer : null,
        mediaRecorder : null,
        audio_source : null,
        base64data : null,
        blobURL : null,
        upload : false,
        desktop : desktop,
        dataChunks : [],
        device : device
    },
    methods: {
        editMarkers : function(question) {
            this.resetB64()
            if (this.marker[question] == 3 ) {
                this.checkMarkers2()
            }
            else{
                this.checkMarkers2()
                this.marker[question] = 3
                // the role of the testOBJ is to store the changes
                //but not the alter the mainOBJ in case the changes are not saved
                let testString = JSON.stringify(this.ansOBJ[question])
                this.testOBJ[question] = JSON.parse(testString)
            }
        },
        resetMarkers : function(q) {
            for (var mark in vue.marker) {
                if (vue.marker[mark] == 3){
                    console.log(vue.ansOBJ, vue.ansOBJ[q])
                    if (mark == q) {
                        alert('Question updated by ' + vue.ansOBJ[q]['user'])
                    }
                }
            }
        },
        checkMarkers: function() {
            for (var mark in vue.marker) {
                if (this.ansOBJ[mark]['user']){
                    vue.marker[mark] = 2
                }
                else {
                    vue.marker[mark] = 1
                }
            }
        },
        checkMarkers2: function() {
            for (var mark in vue.marker) {
                if ( vue.marker[mark] == 3 ){
                    console.log('open question', mark)
                    let reset = true
                    for (var item in vue.ansOBJ[mark]) {
                        console.log('CHECK', vue.ansOBJ[mark][item])
                        if(vue.ansOBJ[mark][item] == null){
                            reset = false
                        }
                    }
                    if ( reset == true ) {
                        vue.marker[mark] = 2
                    }
                }
                else {
                    vue.marker[mark] = 2
                    for (var item in vue.ansOBJ[mark]) {
                        // console.log(mark, item, vue.ansOBJ[mark][item]);
                        if(vue.ansOBJ[mark][item] == null){
                            vue.marker[mark] = 1
                        }
                    }
                }
            }
        },
        qStyle : function(key) {
            return this.buttonColor[this.marker[key]]
        },
        updateAnswers : function() {
            //runs in the background to check if others have changed something
            console.log('update via AJAX');
            $.ajax({

              data : {
                unit : this.unit,
                team : this.team,
                mode : this.mode
              },
              type : 'POST',
              url : '/proupdateAnswers',
            })
            .done(function(data) {
                var newOBJ = JSON.parse(data.ansString)
                for (var q in vue.ansOBJ){
                    // if the strings are not the same then a change has been made
                    if (   JSON.stringify(newOBJ[q]) != JSON.stringify(vue.ansOBJ[q])   ){
                        //alert(JSON.stringify(newOBJ[q]))
                        vue.ansOBJ = newOBJ
                        // reset markers knowing the question that has been changed
                        vue.resetMarkers(q)
                    }
                }
            })
            .fail(function(){
                console.log('error has occurred');
            });
        },
        storeData : function(key) {
            //reset the testOBJ
            this.testOBJ = testOBJ

            this.ansOBJ[key]['user'] = document.getElementById(key +  'u').innerHTML
            this.ansOBJ[key]['question'] = document.getElementById(key + 'q').value
            this.ansOBJ[key]['answer1'] = document.getElementById(key + 'a1').value
            this.ansOBJ[key]['answer2'] = document.getElementById(key + 'a2').value

            this.checkMarkers2()

            console.log(this.ansOBJ[key])

            $.ajax({
              data : {
                unit : this.unit,
                team : this.team,
                mode : this.mode,
                ansOBJ : JSON.stringify(this.ansOBJ),
                question : key,
              },
              type : 'POST',
              url : '/prostoreAnswer',
            })
            .done(function(data) {
                console.log(data);
                vue.updateAnswers()
                vue.checkMarkers()
            })
            .fail(function(){
                alert('error - see instructor')
            });
        },
        storeB64 : function(key, b64) {
            //reset the testOBJ
            this.testOBJ = testOBJ
            console.log(key, b64, this.image64['base64'])
            alert('data uploading, please wait')

            if (b64 == 'i1'){
                var b64data = this.image64['base64']
                var fileType = this.image64['fileType']
                // this.ansOBJ[key]['imageLink'] = 'updating'
            } else if (b64 == 'i2') {
                var b64data = this.image64['base64']
                var fileType = this.image64['fileType2']
            } else if (b64 == 'a'){
                var b64data = vue.base64data
                if (this.device == 'I'){
                    b64data = b64d
                }
                var fileType = 'mp3'
                // this.ansOBJ[key]['audioLink'] = 'updating'
            }

            $.ajax({
              data : {
                unit : this.unit,
                team : this.team,
                mode : this.mode,
                b64data : b64data,
                fileType : fileType,
                question : key,
                b64 : b64,
              },
              type : 'POST',
              url : '/prostoreB64',
            })
            .done(function(data) {
                console.log(data);
                alert('Question ' + data.question + ' updated')
                location.reload()
                // vue.reset64()
                // vue.updateAnswers()
                // vue.checkMarkers()
            })
            .fail(function(){
                alert('error - see instructor')
            });
        },
        resetB64 : function() {
            vue.image64['fileType2'] = null
            vue.image64['fileType'] = null
            vue.image64['base64'] = null
            vue.audio64['fileType'] = null
            vue.audio64['base64'] = null
        },
        imageValidation : function(arg){

            if (arg == 1 || arg == null) {
                var fileInput = document.getElementById('image');
                //console.log('file', fileInput)
                var filePath = fileInput.value;
                //console.log(filePath);
                vue.image64['fileType'] = filePath.split('.')[1]
            } else {
                var fileInput = document.getElementById('image2');
                //console.log('file', fileInput)
                var filePath = fileInput.value;
                //console.log(filePath);
                vue.image64['fileType2'] = filePath.split('.')[1]
            }


            var allowedExtensions = /(\.jpeg|\.png|\.jpg)$/i;

            if(fileInput.files[0].size > 7000000){ // 7 mb for video option
                alert("File is too big!");
                fileInput.value = '';
                return false;
            }
            else if(!allowedExtensions.exec(filePath)){
                alert('Please upload image: .jpeg/.png only.');
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
                    var reader = new FileReader();
                    reader.readAsDataURL(savedBlob);
                    reader.onloadend = function() {
                        vue.image64['base64'] = reader.result.split(',')[1];
                        }
                })

              }//end else
          },
        playAudio : function(key){
            player = document.getElementById('handler')
            button = document.getElementById(key)
            player.src = ansOBJ[key]['audioLink']
            player.load()
            button.innerHTML = 'Playing'
          },
        testAudio : function (arg) {

            player = document.getElementById('audio' + arg)
            console.log(vue.blobURL)


            player.src = vue.blobURL

        },
        start : function(task){

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
        vue.rec1.stop = false
        vue.rec1.save = true
        vue.rec1.cancel = true
        clearInterval(vue.rec_timer)
        console.log('STOPPED', task, this.device);

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
            clearInterval(vue.rec_timer)
            console.log('cancel');
            for (var key in vue.rec1){
                vue.rec1[key] = false
            }
            vue.rec1.start = true

            for (var key in vue.showSpeak){
                vue.showSpeak[key] = true
            }
            vue.base64data = null
            vue.blobURL = null
            this.audioCheck()
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



    }, // end methods



})// end NEW VUE

}// endFunction

