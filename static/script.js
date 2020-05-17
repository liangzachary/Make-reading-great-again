function hackAccount() {
  var numbers = $("#inputText").val();
  $.ajax({
    url: "/generate?text=" + numbers,
    success: function (result) {
      console.log("result = " + result);
      $("#result").html(result);


      // document.getElementById("audio_area").innerHTML = ""
      // document.get
      var audio = document.getElementById('audio');
      audio.load()
      // console.log(audio)
      // var source = document.getElementById('audioSource');
      // console.log(source)
      // // source.src = "https://awsmlcomptext-4--yee2.repl.co/audio"
      // source.src = ""
      // var source = document.getElementById('audioSource');


      // audio.load(); //call this to just preload the audio without playing
      // source.src = "../book_home/bookaudio.mp3"
      // audio.load(); //call this to just preload the audio without playing

      // audio.play(); //call this to play the song right away
      // document.getElementById("audio_area").innerHTML = '<audio controls><source src="https://awsmlcomptext-4--yee2.repl.co/audio" type="audio/mpeg"></audio>'
      $.ajax({
        url: "/audio",
        success: function (result) {
          console.log("Getting audio")
          console.log(typeof (result));
          console.log(result)
        }
      })
    },
    error: function (data) {
      console.log("failed");
    }
  });
}