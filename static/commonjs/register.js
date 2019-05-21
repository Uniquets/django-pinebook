
$("#register").click()
{
    console.log("111")
    $.ajax({
         url:"/register/"
        ,type:"post"
        ,dataType:"JSON"
        ,data:$("#regfm").serialize()
        ,success:function(args){
              }
        })
}