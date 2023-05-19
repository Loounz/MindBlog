// 获取文章数据
function getArticles(id){
    console.log('hello');
    $.ajax({
        type:'get',
        url:'http://127.0.0.1:5000/articles/'+String(id),
        success:function(data){
            // 这里data已经转换成js对象了，可以直接操作
            console.log(data);
            html = '<article>';
            title = "<h1>" + data.result['ArticleTitle'] + "</h1>";
            author = "<h2>" + data.result['ArticleAuthor'] + "</h2>";
            content = "<p>" + data.result['ArticleContext'] + "</p>";
            article_end = '</article>';
            console.log(html+title+author+content+article_end);

document.getElementById('left_body').innerHTML = html+title+author+content+article_end;

            return html+title+author+content+article_end;
        }
    })
}

// 获取所有文章信息
function getAllArticles(){
    for(var i = 0;i < 50;++i){
        getArticles(i);
    }
}

