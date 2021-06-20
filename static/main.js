// ------- custom js -------- //

//hide initial
$("#searching").hide();
$("#results-table").hide();
$("#error").hide();
$("#done").hide();

let url = "http://127.0.0.1:5000/static/dataset/";
let data = [];

$(function (){
   $(".img").click(function (){
       $("#searching").hide();
       $("#results-table").hide();
       $("#error").hide();
       $("#done").hide();
       $(".img").removeClass("active");
       $(this).addClass("active");
       let image = $(this).attr("src");
       $("#searching").show();
       $.ajax({
          type: "POST",
          url: "/search",
          data: {img : "http://127.0.0.1:5000/" + image},
          success: function (result){
              console.log(result.results)
              let data = result.results;
              $("#results-table").show();
              // loop through results, append to dom
              $("#results").empty();
              for (let i = 0; i < data.length; i++) {
                  $("#results").append('<tr><th><a href="'+url+data[i]["image"]+'"><img src="'+url+data[i]["image"]+
                    '" class="result-img"></a></th><th>'+data[i]['score']+'</th></tr>');
              };
          },
          error: function (error){
              console.log(error);
              $("#error").append();
          }
       });
       $("#searching").hide();
       $("#done").show();
   });
});

