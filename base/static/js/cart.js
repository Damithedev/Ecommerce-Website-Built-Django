var updatebtns = document.getElementsByClassName('update-cart')

function addtocart() {
    console.log("lesss hooo")
    var popup = document.getElementById('popupz')
    popup.style.display = "block"
    setTimeout(function () {
        popup.style.display = "none"

    }, 1500)
}

for(var i =0; i< updatebtns.length; i++){
    updatebtns[i].addEventListener('click', function () {
        var pid = this.dataset.product;
        var productquantity = "{{}}"
        var action =  this.dataset.action

        console.log(pid);
        console.log(user);
        if(user === "AnonymousUser"){
            console.log("Not Authenticated")
        }
        else {


            updateuserorder(pid,action)
        }


    })
}
function updateuserorder(pid, action) {
    console.log("Sending data.....");
    var url ='/updateitem';
    var itemquant = document.getElementById(pid)
    var price=document.getElementById(pid+'price')
    var cartsum =  document.getElementById('totalsum')

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-type':'application/json',
            "X-CSRFToken": getCookie("csrftoken")

        },
        body:JSON.stringify({'pid': pid , 'action':action}),


    })
        .then(value => value.json())
        .then(function (value) {
            itemquant.innerText = value['quantity']
            if (itemquant.innerText <= 0){
                location.reload()
            }
            price.innerText = "₦" +value['sum']
            cartsum.innerText = value['cartsum']
        })

}




