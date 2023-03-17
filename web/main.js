document.addEventListener('DOMContentLoaded',()=>{eel.loadImages()},false)

eel.expose(loadImages)
function loadImages(imagesnames) {
    for(let name of imagesnames){
        document.getElementById("images").innerHTML+="<img src=images/"+name+" width=100>";
    }
}