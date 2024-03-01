
  document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('startInteraction').addEventListener('click', function() {
        // Inicia o reconhecimento de fala
        recognition.start();
        console.log("Interação iniciada pelo botão.");
    });
  });


var isOnKWS=false;
const sensor = new MicrophoneSensor();
  let classifyCache = {};
  let allData = [];
  let allClassifications = [];
  let casa_vivaStarted = null;

// Start the KEYWORD SPOTTING
async function startkws(){
  classifyCache = {};
  allData = [];
  allClassifications = [];
  casa_vivaStarted = null;

  isOnKWS=false;
  //await sensor.takeSample(200, 16000, () => {});
  sensor.takeSample(1000, 16000, () => {}).then(onSampleComplete);
}

// Clear the cache every hour
setTimeout(function(){
  classifyCache = {};
  allData = [];
  allClassifications = [];
  casa_vivaStarted = null;
}, 60*60*1000);

// Load the model
const onSampleComplete = (obj) => {
    if(!isOnKWS)
    sensor.takeSample(500, 16000, () => {}).then(onSampleComplete);

    allData = allData.concat(obj.values);
    //console.log(Date.now(), 'allData is', allData.length / 16000, 'seconds');

    const windowSize = 3 * 16000;
    const windowStep = 0.5 * 16000;
    const classifyWindowLength = 0.5 * 16000;
    const classifyWindowOverlap = 0.25 * 16000;

    // if we have at least one window of data...
    if (allData.length >= windowSize) {
      let window = allData.slice(allData.length - windowSize, allData.length);

      let noiseCount = 0;
      let casa_vivaCount = 0;
      let uncertainCount = 0;

      // in here we'll take 1 second slices, with 300 ms. overlap that we then classify (total 14 windows)
      console.time('classifyWindow');
      for (let wx = 0; wx <= windowSize - classifyWindowLength; wx += classifyWindowOverlap) {
        const cacheKey = allData.length - windowSize + wx;

        let classifyResult;
        if (!classifyCache[cacheKey]) {
            let slice = window.slice(wx, wx + classifyWindowLength);

            classifyCache[cacheKey] = classifier.classify(slice, false);
        }

        classifyResult = classifyCache[cacheKey];
        let noise = classifyResult.results.find(r => r.label === 'noise').value;
        let casa_viva = classifyResult.results.find(r => r.label === 'casa_viva').value;

if(casa_viva>.3)
        console.log(casa_viva);
        if (noise >= 0.6) {
            noiseCount++;
        }
        else if (casa_viva >= 0.6) {
            casa_vivaCount++; 
            
            if(!isOnKWS){
              recognition.start();
              circle.animate(20, 0, 'now').attr({ fill: '#00a431' });
              transcriptDiv.textContent = "...";
              isOnKWS=true;
            }
              
        }
        else {
            uncertainCount++;
        }
      }
    }
    //console.timeEnd('classifyWindow');
  };

// Initialize the KWS
async function InitializeKWS(){
  const classifier = window.classifier = new EdgeImpulseClassifier();
  await classifier.init();
  await sensor.init();
  if (!sensor.hasSensor()) {
    alert('Your device does not seem to have a microphone');
  }
  // start up the sensor
  //await sensor.takeSample(200, 16000, () => {});

  // then take 1s of data
  sensor.takeSample(500, 16000, () => {}).then(onSampleComplete);
};
InitializeKWS();


  import { interpolateGreens } from "https://cdn.skypack.dev/d3-scale-chromatic@3"

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition(); //new webkitSpeechRecognition();
  recognition.continuous = false; 
  recognition.interimResults = true;
  recognition.lang = 'pt-PT';


  var circle = SVG.find('.st0');//.fill('#ccc');    
  const startBtn = document.getElementById('start-btn');
  const transcriptDiv = document.getElementById('transcript');
  const energyDiv = document.getElementById('energy');

  var firstSent = "Diga 'Casa Viva' para comecar a falar.";
  transcriptDiv.textContent = firstSent;
  var resetfunc ;


  recognition.onerror = function(event) {
    console.error("REC ERROR"+event.error);
    transcriptDiv.innerHTML = firstSent;
    circle.animate(20, 0, 'now').attr({ fill: '#000' });
    startkws();
  };

  recognition.onresult = function(event) {
    speechActive=false;
    var interim_transcript = '';
    var final_transcript = '';

    for (var i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        //if(event.results[i][0].confidence>0.6)
        energyDiv.textContent += event.results[i][0].confidence;
        {
          final_transcript ="";
          console.log("++"+event.results[i][0].transcript+"++");
          final_transcript=event.results[i][0].transcript.trim();
          /*var sentence = event.results[i][0].transcript.trim().toLowerCase();
          if(sentence.startsWith("casa viva") || sentence.startsWith("viva") || sentence.startsWith("aviva") || sentence.startsWith("sa viva") || sentence.startsWith("da viva") ||sentence.startsWith("ora viva"))
          {
            var indSent = sentence.indexOf("viva");
            final_transcript= sentence.slice(indSent+5);
          }*/
        }

        if(final_transcript.length>2){
          final_transcript = final_transcript.charAt(0).toUpperCase()+ final_transcript.slice(1);
          transcriptDiv.innerHTML = "<span style='color:#00b44e'><b>"+final_transcript+"</b></span>";

          sendMMI(final_transcript);
          circle.animate(20, 0, 'now').attr({ fill: '#000' });
          startkws();
        }else{
          transcriptDiv.innerHTML = "<span style='color:#ff9494'><b>Desculpe nao consegui ententer.</b></span>";
        }

        resetfunc = setTimeout(function(){
          transcriptDiv.innerHTML = firstSent;
        }, 3000);

        speechActive = false;
      }else{
        //if(event.results[i][0].confidence>0.6)
        {
          console.log(event.results[i][0].transcript + " -- " + i);
          var sentence = event.results[i][0].transcript.trim().toLowerCase();
          /*if(sentence.startsWith("casa viva") || sentence.startsWith("viva") || sentence.startsWith("aviva") || sentence.startsWith("sa viva") || sentence.startsWith("da viva") ||sentence.startsWith("ora viva") ){
            var indSent = sentence.indexOf("viva");
            final_transcript= sentence.slice(indSent+5);
          }*/

        }
        transcriptDiv.textContent = event.results[i][0].transcript.trim().toLowerCase();
      }
    }
  };


  var vadActive = false;
  var speechActive = false;

  async function main() {
    const myvad = await vad.MicVAD.new({

      onSpeechEnd: (audio) => {
        // do something with `audio` (Float32Array of audio samples at sample rate 16000)...
        //transcriptDiv.textContent += "-";
        vadActive = false;
        setTimeout(function(){
          if(speechActive) recognition.stop();
          speechActive=false;
        }, 3000);
      },
      onSpeechStart: ()=>{
        //transcriptDiv.textContent += " ->";
        if(!speechActive){
          speechActive=true;
          recognition.start();
          transcriptDiv.textContent = "...";
        }
        clearTimeout(resetfunc);
        vadActive=true;
      },
      onFrameProcessed: (probs) => {
        if(vadActive || speechActive){
          const indicatorColor = interpolateGreens(probs.isSpeech / 1.5);
          //circle.fill(indicatorColor);
          circle.animate(20, 0, 'now').attr({ fill: indicatorColor });
        } 
        //    energyDiv.textContent = probs.isSpeech + "--" + probs.notSpeech;  
        //document.body.style.setProperty("--indicator-color", indicatorColor)
      },
    })
    //myvad.start()
  }
  main()

  if ('speechSynthesis' in window) {
	  console.log('Your browser <strong>supports</strong> speech synthesis.');
  }

  var ttsSpeaker;
  window.speechSynthesis.onvoiceschanged = function(e) {
    var voices = speechSynthesis.getVoices();
    ttsSpeaker = voices[0];
    for (let i = 0; i < voices.length; i++) {
      if(voices[i].lang=="pt-PT"){
        console.log(voices[i]);
        if(voices[i].name.includes("Duarte")) ttsSpeaker=voices[i];
      }
    }
    console.log(ttsSpeaker);
  };
  
  function speak(text){

    var msg = new SpeechSynthesisUtterance();
    msg.text = text;
  
    // Set the attributes.
    msg.volume = parseFloat(1);
    msg.rate = parseFloat(1.1);
    msg.pitch = parseFloat(1);

    msg.voice = ttsSpeaker;

    window.speechSynthesis.speak(msg);
  }
  /////////////////////////////////////////


  var mmiCli_1 = null;
  mmiCli_1 = new MMIClient(null, mmi_fusion + "SPEECHIN");



  // ---------------------------------------------------------------------------------------------------------------
  // | UNICO SPOT PARA ALTERAÇÕES - KITCHEN ASSISTANT FOR ACTIVE AGEING !!!!!                                      |
  // |                                                               - KITCHEN ASSISTANT FOR ACTIVE AGEING !!!!!   |
  // ---------------------------------------------------------------------------------------------------------------
  function sendMMI(final_transcript){

    var obj = new Object();
    var recipe ;
    obj.text = final_transcript;
    console.log("FINAL TRANSCRIPT: "+final_transcript);
    $.post( "http://localhost:5005/model/parse", JSON.stringify(obj), function( data ) {
    console.log(data);
    //console.log("INTENT: "+data.intent.name);
    //console.log("ENTITY NAME: "+data.entities[0].entity);
    //console.log("ENTITY VALUE: "+data.entities[0].value);
    switch(data.intent.name){
      case "ask_specific_recipe": // ---------------------------------------------------------------------- [ ASK_SPECIFIC_RECIPE]+
        /*for (let i = 0; i < data.entities.length; i++)
        {
          if(data.entities[i].entity=='recipe')
            console.log("ENTIDADE ISIDE FOR: "+data.entities[i]);
            console.log("ENTIDADE_VALOR ISIDE FOR: "+data.entities[i].value);
            recipe = data.entities[i].value;
            console.log("RECIPE: "+recipe);
        }*/
        var message = {'intent':'ask_spefific_recipe','recipe':data.entities[0].value , 'audioReconized': final_transcript }
        var messaget = btoa(unescape(encodeURIComponent(final_transcript)));
        var result = { "recognized" : ["SPEECH", "SPEECHIN", "APP"], "text": messaget, "nlu": message };
        mmiCli_1.sendToIM(new LifeCycleEvent("SPEECHIN", "IM", "text-1", "ctx-1").
              doExtensionNotification(new EMMA("text-", "text", "command", 1, 0).
              setValue(JSON.stringify(result))));
        break;
      case "greet": // ------------------------------------------------------------------------------------- [ GREET]
        var message = {'intent':'greet', 'audioReconized': final_transcript }
        var messaget = btoa(unescape(encodeURIComponent(final_transcript)));
        var result = { "recognized" : ["SPEECH", "SPEECHIN", "APP"], "text": messaget, "nlu": message};
        mmiCli_1.sendToIM(new LifeCycleEvent("SPEECHIN", "IM", "text-1", "ctx-1").
              doExtensionNotification(new EMMA("text-", "text", "command", 1, 0).
              setValue(JSON.stringify(result))));
        break;
      case "goodbye": // ----------------------------------------------------------------------------------- [ GOODBYE]
        var message = {'intent':'goodbye', 'audioReconized': final_transcript }
        var messaget = btoa(unescape(encodeURIComponent(final_transcript)));
        var result = { "recognized" : ["SPEECH", "SPEECHIN", "APP"], "text": messaget, "nlu": message };
        mmiCli_1.sendToIM(new LifeCycleEvent("SPEECHIN", "IM", "text-1", "ctx-1").
              doExtensionNotification(new EMMA("text-", "text", "command", 1, 0).
              setValue(JSON.stringify(result))));
        break;
      case "ask_random_recipe": // -------------------------------------------------------------------------- [ ASK_RANDOM_RECIPE]
        var message = {'intent':'ask_random_recipe', 'audioReconized': final_transcript }
        var messaget = btoa(unescape(encodeURIComponent(final_transcript)));
        var result = { "recognized" : ["SPEECH", "SPEECHIN", "APP"], "text": messaget, "nlu": message };
        mmiCli_1.sendToIM(new LifeCycleEvent("SPEECHIN", "IM", "text-1", "ctx-1").
              doExtensionNotification(new EMMA("text-", "text", "command", 1, 0).
              setValue(JSON.stringify(result))));
        break;
      case "affirm": // ------------------------------------------------------------------------------------- [ AFFIRM]
        var message = {'intent':'affirm', 'audioReconized': final_transcript }
        var messaget = btoa(unescape(encodeURIComponent(final_transcript)));
        var result = { "recognized" : ["SPEECH", "SPEECHIN", "APP"], "text": messaget, "nlu": message};
        mmiCli_1.sendToIM(new LifeCycleEvent("SPEECHIN", "IM", "text-1", "ctx-1").
              doExtensionNotification(new EMMA("text-", "text", "command", 1, 0).
              setValue(JSON.stringify(result))));
        break;
      case "deny": // --------------------------------------------------------------------------------------- [ DENY]
        var message = {'intent':'deny', 'audioReconized': final_transcript }
        var messaget = btoa(unescape(encodeURIComponent(final_transcript)));
        var result = { "recognized" : ["SPEECH", "SPEECHIN", "APP"], "text": messaget, "nlu": message };
        mmiCli_1.sendToIM(new LifeCycleEvent("SPEECHIN", "IM", "text-1", "ctx-1").
              doExtensionNotification(new EMMA("text-", "text", "command", 1, 0).
              setValue(JSON.stringify(result))));
        break;
      case "ask_repeat_step": // ----------------------------------------------------------------------------- [ ASK_REPEAT_STEP]
        var message = {'intent':'ask_repeat_step', 'audioReconized': final_transcript }
        var messaget = btoa(unescape(encodeURIComponent(final_transcript)));
        var result = { "recognized" : ["SPEECH", "SPEECHIN", "APP"], "text": messaget, "nlu": message };
        mmiCli_1.sendToIM(new LifeCycleEvent("SPEECHIN", "IM", "text-1", "ctx-1").
              doExtensionNotification(new EMMA("text-", "text", "command", 1, 0).
              setValue(JSON.stringify(result))));
        break;
        case "ask_first_step": // ----------------------------------------------------------------------------- [ ASK_FIRST_STEP]
        var message = {'intent':'ask_first_step', 'audioReconized': final_transcript }
        var messaget = btoa(unescape(encodeURIComponent(final_transcript)));
        var result = { "recognized" : ["SPEECH", "SPEECHIN", "APP"], "text": messaget, "nlu": message };
        mmiCli_1.sendToIM(new LifeCycleEvent("SPEECHIN", "IM", "text-1", "ctx-1").
              doExtensionNotification(new EMMA("text-", "text", "command", 1, 0).
              setValue(JSON.stringify(result))));
        break;
        case "ask_next_step": // ----------------------------------------------------------------------------- [ ASK_NEXT_STEP]
        var message = {'intent':'ask_next_step', 'audioReconized': final_transcript }
        var messaget = btoa(unescape(encodeURIComponent(final_transcript)));
        var result = { "recognized" : ["SPEECH", "SPEECHIN", "APP"], "text": messaget, "nlu": message };
        mmiCli_1.sendToIM(new LifeCycleEvent("SPEECHIN", "IM", "text-1", "ctx-1").
              doExtensionNotification(new EMMA("text-", "text", "command", 1, 0).
              setValue(JSON.stringify(result))));
        break;
      case "joke":  // -------------------------------------------------------------------------------------- [ JOKE]
        var message = {'intent':'joke', 'audioReconized': final_transcript }
        var messaget = btoa(unescape(encodeURIComponent(final_transcript)));
        var result = { "recognized" : ["SPEECH", "SPEECHIN", "APP"], "text": messaget, "nlu": message};
        mmiCli_1.sendToIM(new LifeCycleEvent("SPEECHIN", "IM", "text-1", "ctx-1").
              doExtensionNotification(new EMMA("text-", "text", "command", 1, 0).
              setValue(JSON.stringify(result))));
        break;
      case "ask_recipe_instructions":
        break;
      case "default":
        break;
    }
  // ---------------------------------------------------------------------------------------------------------------
  // | UNICO SPOT PARA ALTERAÇÕES - KITCHEN ASSISTANT FOR ACTIVE AGEING !!!!!                                      |
  // |                                                               - KITCHEN ASSISTANT FOR ACTIVE AGEING !!!!!   |
  // ---------------------------------------------------------------------------------------------------------------

    /* if(data.intent.name=='change_color'){
      var shape='' ;
      var color='' ;

      for (let i = 0; i < data.entities.length; i++)
      {
        if(data.entities[i].entity=='shape')
    	    shape=data.entities[i].value;
        if(data.entities[i].entity=='color')
    	    color=data.entities[i].value;
      }
    
      var message = {'intent':'change_color','shape':shape,'color':color}
      var messaget = btoa(unescape(encodeURIComponent(final_transcript)));
      var result = { "recognized" : ["SPEECH", "SPEECHIN", "APP"], "text": messaget, "nlu": message };
      mmiCli_1.sendToIM(new LifeCycleEvent("SPEECHIN", "IM", "text-1", "ctx-1").
            doExtensionNotification(new EMMA("text-", "text", "command", 1, 0).
            setValue(JSON.stringify(result))));
    }
    */
  });

  /*
    
            */
  }
 // sendMMI("mudar para azul o circulo");
  

  var mmiCli_Out_add = "wss://"+host+":8005/IM/USER1/";
  var mmiCli_Out = null;
  mmiCli_Out = new MMIClientSocket(mmiCli_Out_add + "SPEECHOUT");
  mmiCli_Out.onMessage.on(im1MessageHandler);
  mmiCli_Out.onOpen.on(socketOpenHandler);
	mmiCli_Out.openSocket();


  function socketOpenHandler(event) {
    console.log("---------------openSocketHandler---------------")

    if(mmiCli_Out.socket.readyState !== WebSocket.OPEN)
    {
        return;
    }
  }

  function im1MessageHandler(data) {

    console.log("--------------im1MessageHandler---------------");

    if(data != null && data!="RENEW" && data!="OK") {

      console.log(data);

      var content = $(data).find("emma\\:interpretation").first().text().trim();

      if (typeof content == 'string') {
        try {
          // Try to parse XML
          var xml = $.parseXML(content.replace(/\\"/g, "\"").slice(1,-1));

          // Extract sentence
          let text = $(xml).find("p").text();
          //let text = Utf8.decode(atob(sentence.slice(2,-1)));

          console.log(text);
          speak(text);

          $("#response").html(text);
          $("#response").addClass("container");
          $("#response").addClass("responseText");

          setTimeout(function(){
            $("#response").html("");
            $("#response").removeClass("container");
            $("#response").removeClass("responseText");
          }, 3000);

        }
        catch (e) { console.log(e); }

      }
    }
  }

