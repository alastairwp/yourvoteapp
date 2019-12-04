setInterval(function () {
           var url = '/get_chart_data';
           var question_id = $('#question_id').val();
           var course_id = $('#course_id').val();
           var course_status = $('#course_status').val();
           var vote_count = $('#vote_count').val();

           votelabel =
           $.ajax({
               url: url,
               type: "POST",
               data:{question_id:question_id, course_id:course_id, vote_count:vote_count, course_status:course_status, csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()},
               success: function (result) {
                   var xvalue = new Array();
                   var votes = [1,2,3,4,5,6,7,8,9];
                   result.alldata.forEach(function (item,key) {
                        if(course_status==0){
                            var x = item.fields.value;
                        } else {
                            var x = item.fields.revised_value;
                        }

                       xvalue.push(x);
                       // console.log(x);
                   });

                   var cheknewarray = new Array();
                   votes.forEach(function (item,key) {
                       var i =0;
                       xvalue.forEach(function (itemdata,keydata) {
                          if(itemdata==item){
                            i = i+1;
                          }
                       })

                       cheknewarray.push(i);
                   })
                    voted_users_list = result.voted_users.toString();
                    not_voted_users_list = result.not_voted_users.toString();
                    document.getElementById("vote_label").innerHTML = "Showing " + result.vote_count + " votes";
                    if (document.getElementById("voted_users")) {
                        document.getElementById("voted_users").innerHTML = voted_users_list.replace(/,/g, '');
                        }
                    if (document.getElementById("not_voted_users")) {
                        document.getElementById("not_voted_users").innerHTML = not_voted_users_list.replace(/,/g, '');
                        }
                    drawChart(votes,cheknewarray);
                   }
               });
        },1000);

function drawChart(x,y) {
    var trace = {
        x: x,
        y: y,
        type: 'bar',
        marker: {
            color: ['#ff0000', '#f92d06', '#f35a0b', '#ed8711', '#e7b416', '#adc711', '#74da0b', '#3aec06', '#00ff00']
        },
    };
   var layout = {
       autosize: true,
       xaxis: {
           tickangle: 0,
           showticklabels: true,
           type: 'category',
           title: 'Vote'
       },
       yaxis: {
           tickangle: 0,
           showticklabels: true,
           title: 'Count',
           dtick: 1,
       },
       margin: {
           l: 75,
           r: 0,
           b: 75,
           t: 30,
           pad: 0
       },
       font: {
           family: 'Arial, sans-serif',
           size: 20
       },
       showlegend: false

   };

   Plotly.newPlot('chart', [trace], layout, {
       scrollZoom: false,
       displayModeBar: false,
   });
}



     // using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

