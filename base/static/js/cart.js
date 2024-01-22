var updatebtns = document.getElementsByClassName('update-cart')
var popup = document.getElementById('popupz')
function addtocart() {
    console.log("lesss hooo")
    popup.innerText = 'Item added to cart'
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

        updateuserorder(pid,action)



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
             if(value['response'] === 'Max quantity exceeded'){
popup.innerText = value['response']

                 popup.style.display = "block"

    setTimeout(function () {
        popup.style.display = "none"


    }, 1500)
            }
            else {
                 console.log('Reached the else block');

                 itemquant.innerText = value['quantity']
                 if (itemquant.innerText <= 0) {
                     location.reload()
                 }
                 price.innerText = "₦" + value['sum']
                 cartsum.innerText = value['cartsum']
             }
        })

}




