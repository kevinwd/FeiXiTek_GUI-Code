window.onload=function () {
    let statusArr = document.getElementsByClassName("statusBGC");
    let engineArr = document.getElementsByClassName("engineBGC");
    let uptimeArr = document.getElementsByClassName("uptimeBGC");
    let alertArr = document.getElementsByClassName("alertBGC");
    let masterArr = document.getElementsByClassName("masterBGC");
    let mirrorArr = document.getElementsByClassName("mirrorBGC");

    for(let i=0; i<statusArr.length; i++) {

        if (statusArr[i].innerHTML === "ONLINE") {
            statusArr[i].style.backgroundColor = "#dff0d8";
            engineArr[i].style.backgroundColor = "#dff0d8";
            uptimeArr[i].style.backgroundColor = "#dff0d8";
            alertArr[i].style.backgroundColor = "#dff0d8";
            mirrorArr[i].style.backgroundColor = "#dff0d8";
            masterArr[i].style.backgroundColor = "#dff0d8";
        }else {
            statusArr[i].style.backgroundColor = "#EE7621";
            engineArr[i].style.backgroundColor = "#EE7621";
            uptimeArr[i].style.backgroundColor = "#EE7621";
            alertArr[i].style.backgroundColor = "#EE7621";
            mirrorArr[i].style.backgroundColor = "#EE7621";
            masterArr[i].style.backgroundColor = "#EE7621";
        }
    }
    for(let i=0; i<alertArr.length; i++) {

        if (alertArr[i].innerHTML === "None") {
            statusArr[i].style.backgroundColor = "#dff0d8";
            engineArr[i].style.backgroundColor = "#dff0d8";
            uptimeArr[i].style.backgroundColor = "#dff0d8";
            alertArr[i].style.backgroundColor = "#dff0d8";
            mirrorArr[i].style.backgroundColor = "#dff0d8";
            masterArr[i].style.backgroundColor = "#dff0d8";
        }else {
            statusArr[i].style.backgroundColor = "#EE7621";
            engineArr[i].style.backgroundColor = "#EE7621";
            uptimeArr[i].style.backgroundColor = "#EE7621";
            alertArr[i].style.backgroundColor = "#EE7621";
            mirrorArr[i].style.backgroundColor = "#EE7621";
            masterArr[i].style.backgroundColor = "#EE7621";
        }
    }
}


$(function () { $("[data-toggle='tooltip']").tooltip(); });


$(function (obj){
var a = {{signal}};
if ( a === 1 ){
        $("#test").attr("class","alert alert-TC alert-dismissable ")
}else if( a === 0){
$("#test").attr("class","alert alert-TC alert-dismissable hide")
}
        }
)


$("#searchBtn").on("click", function () {
    var value = $("#searchInput").val();
    alert('暂无'+value+'相关内容');
})


