var sounds = {
  "fbk_1" : {
    url : "sounds/fbk_1.wav"
  },
  "fbk_2" : {
    url : "sounds/fbk_2.wav"
  },
  "fbk_3" : {
    url : "sounds/fbk_3.wav"
  },
  "fbk_4" : {
    url : "sounds/fbk_4.wav"
  },
  "fbk_5" : {
    url : "sounds/fbk_5.wav"
  },
  "fbk_6" : {
    url : "sounds/fbk_6.wav"
  },
  "mazili_1" : {
    url : "sounds/mazili_1.wav",
  },
  "mazili_2" : {
    url : "sounds/mazili_2.wav",
  },
  "mazili_3" : {
    url : "sounds/mazili_3.wav",
  },
  "mazili_4" : {
    url : "sounds/mazili_4.wav",
  },
  "mazili_5" : {
    url : "sounds/mazili_5.wav",
  },
  "mazili_6" : {
    url : "sounds/mazili_6.wav",
  },
  "mix_1" : {
    url : "sounds/mix_1.wav"
  },
  "mix_2" : {
    url : "sounds/mix_2.wav"
  },
  "mix_3" : {
    url : "sounds/mix_3.wav"
  },
  "mix_4" : {
    url : "sounds/mix_4.wav"
  },
  "mix_5" : {
    url : "sounds/mix_5.wav"
  },
  "mix_6" : {
    url : "sounds/mix_6.wav"
  }
};


var soundContext = new AudioContext();

for(var key in sounds) {
  loadSound(key);
}

function loadSound(name){
  var sound = sounds[name];

  var url = sound.url;
  var buffer = sound.buffer;

  var request = new XMLHttpRequest();
  request.open('GET', url, true);
  request.responseType = 'arraybuffer';

  request.onload = function() {
    soundContext.decodeAudioData(request.response, function(newBuffer) {
      sound.buffer = newBuffer;
    });
  }

  request.send();
}

function playSound(name, options){
  var sound = sounds[name];
  var soundVolume = sounds[name].volume || 1;

  var buffer = sound.buffer;
  if(buffer){
    var source = soundContext.createBufferSource();
    source.buffer = buffer;

    var volume = soundContext.createGain();

    if(options) {
      if(options.volume) {
        volume.gain.value = soundVolume * options.volume;
      }
    } else {
      volume.gain.value = soundVolume;
    }

    volume.connect(soundContext.destination);
    source.connect(volume);
    source.start(0);
  }
}
