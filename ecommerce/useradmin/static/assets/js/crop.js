const imagebox=document.getElementById('image-box')
const input=document.getElementById('image-id')
const csrf=document.getElementsByName("csrfmiddleware")

input.addEventListener('change',() =>{
    const image_data=input.files[0]
    const url=URL.createObjectURL(image_data)
    imagebox.innerHTML=`<img src="${url}" id="image" width="400px"> `


    var $image = $('#image');
    console.log("helooo")
        $image.cropper({
            aspectRatio: 16 / 9,
            crop: function(event) {
                console.log(event.detail.x);
                console.log(event.detail.y);
                console.log(event.detail.width);
                console.log(event.detail.height);
                console.log(event.detail.rotate);
                console.log(event.detail.scaleX);
                console.log(event.detail.scaleY);
            }
    });
console.log("end")
// Get the Cropper.js instance after initialized
var cropper = $image.data('cropper');
})


