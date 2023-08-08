$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true, 
        margin: 20, 
            responsiveClass: true,
    responsive: {
        0: {
            items: 2,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 4,
            nav: true,
            autoplay: true, 
        }, 
        1000: {
            items: 6,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    $.ajax({
        type: "GET",
        url: "/plus-cart",
        data: {
            prod_id: id
        },
        success: function (data) {
            // eml.innerText = data.quantity
            eml.text(data.quantity);
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
        },
        error: function (xhr, textStatus, errorThrown) {
            console.error("AJAX request failed:", errorThrown);
        }
    })
})

$('.minus-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    $.ajax({
        type: "GET",
        url: "/minus-cart",
        data: {
            prod_id: id
        },
        success: function (data) {
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
        }
    })
})


$('.remove-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this
    $.ajax({
        type: "GET",
        url: "/remove-cart",
        data: {
            prod_id: id
        },
        success: function (data) {
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})



$('.plus-wishlist').click(function () {
    var id = $(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url: "/pluswishlist",
        data: {
            prod_id: id
        },
        success: function (data) {
            //alert(data.message)
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})


$('.minus-wishlist').click(function () {
    var id = $(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url: "/minuswishlist",
        data: {
            prod_id: id
        },
        success: function (data) {
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})

$('.buy-now-btn').click(function() {
    var product_id = $(this).data('product-id');
    $.ajax({
        type: "GET",
        url: `/buy-now/${product_id}/`,
        success: function(data) {
            // Access product_image_url from the JSON response
            var product_image_url = data.product_image_url;
            // Do something with the product_image_url, e.g., display the image
            $('#product-image').attr('src', product_image_url);
            // Redirect to the cart page
            window.location.href = "/cart/";
        }
    });
});

