setInterval(function () {
               var url = '/get_chart_data';
               var question_id = $('#question_id').val();
               var course_id = $('#course_id').val();
               $.ajax({
                   url: url,
                   type: "POST",
                   data:{question_id:question_id, course_id:course_id, csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()},
                   success: function (result) {
                       var xvalue = new Array();
                       var votes = [1,2,3,4,5,6,7,8,9];
                       result.alldata.forEach(function (item,key) {
                            var x = item.fields.value
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

                        drawChart(votes,cheknewarray)
                   }
               });
       },500);

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
                   title: 'Vote score'
               },
               yaxis: {
                   tickangle: 0,
                   showticklabels: true,
                   title: 'Count',
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


       $('document').ready(function () {

           $('.vote-radio').click(function () {
               var valueget = $(this).attr('data-type');
               var question_id = $('#question_id').val();
               var next_iddata  = $('#next_id').val();
               var back_iddata  = $('#back_id').val();
               var question_comment = $('#UserComment').val();
               var course_id = $('#course_id').val();
               var url = '/save_vote_data';
               $.ajax({
                   url: url,
                   type: "POST",
                   data: {question_id:question_id,value:valueget,question_comment:question_comment,course_id:course_id,csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()},
                   success: function (result) {
                       console.log(result)
                       if(result.resultdata==1){
                           if(next_iddata!=''){
                             window.location.href = 'benchmark?id_data='+question_id;
                          }
                       }
                   }
               });
           });
       });


       function savecomment(id) {
            var question_id = $('#question_id').val();
            var next_iddata  = $('#next_id').val();
            var back_iddata  = $('#back_id').val();
            var question_comment = $('#UserComment').val();
            var course_id = $('#course_id').val();
            var url = '/save_comment_data';
               $.ajax({
                   url: url,
                   type: "POST",
                   data: {question_id:question_id,question_comment:question_comment,course_id:course_id,csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()},
                   success: function (result) {
                       console.log(result)
                       if(result.resultdata==1){
                           if(next_iddata!=''){
                             window.location.href = 'benchmark?id_data='+id;
                          }
                       }
                   }
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