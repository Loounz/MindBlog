    // 通过id获取input里的数据
    function getinput(idstr){
        return jQuery("#"+idstr).val();
    }

    // 获取用户数据
    function getuserinfo(id){
        console.log("http://127.0.0.1:5000/articles/"+String(id));
        $.ajax({
            type : "get",
            url : "http://127.0.0.1:5000/articles/"+String(id),
            success: function(data){
                console.log(data);
            }
        })
    }