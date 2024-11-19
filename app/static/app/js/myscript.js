$('.plus-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];  // Target the quantity span
    
    $.ajax({
        type: "GET",
        url: updateCartUrl,
        data: {
            prod_id: id,
            action: 'increase'
        },
        success: function(data) {
            eml.innerText = data.quantity;
            document.getElementById("amount").innerText = 'Rs. ' + data.amount;
            document.getElementById("totalamount").innerText = 'Rs. ' + data.totalamount;
        }
    });
});

$('.plus-wishlist').click(function(){
    var id = $(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/pluswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            window.location.reload();
        }
    })
})

$('.minus-wishlist').click(function(){
    var id = $(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/minuswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            window.location.reload();
        }
    })
})