


startVue(ansOBJ, device)

function startVue(ansOBJ, device){

  let vue = new Vue({

    el: '#vue-app',
    delimiters: ['[[', ']]'],
    mounted: function () {
      this.audioCheck()
    },
    data: {

        notice : notice,
        showSpeak: {
          1 : true,
          2 : true,
          3 : true
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
        audio_source : null,
        base64data : null,
        blobURL : null,
        upload : false,
        desktop : desktop,
        dataChunks : []
    },
    methods: {
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

    } // end methods



  })// end NEW VUE

}// endFunction



