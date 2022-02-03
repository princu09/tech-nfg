function changeImg(smallImg) {
    var fullImg = document.getElementById("imageBox");
    fullImg.src = smallImg.src;
}
$(document).ready(function() {
    rate = []
    rating = $('.rating').text();
    for (let i = 0; i < rating; i++) {
        rate.push('<i class="fas fa-star"></i>')
    }
    if (rate.length < 5) {
        addBlankStar = 5 - rate.length
        for (let i = 0; i < addBlankStar; i++) {
            rate.push('<i class="fal fa-star"></i>')
        }
        $('.rating').html(rate);
    }

    $(function() {
        $('[data-toggle="popover"]').popover({ html: true });

    })
    popStr = '<i class="far fa-frown"></i> Cart Empty'
    popOver = document.getElementById('popOver').setAttribute('data-content', popStr);

})


if (localStorage.getItem('cart') == null) {
    var cart = {};
} else {
    cart = JSON.parse(localStorage.getItem('cart'));
    updateCart(cart);
}


// $('.cart').click(function () {
$('.product').on('click', 'button.cart', function() {
    var idstr = this.id.toString();
    if (cart[idstr] != undefined) {
        qty = cart[idstr][0] + 1;
    } else {
        qty = 1;
        name = document.getElementById('name' + idstr).innerHTML;
        itemPrice = document.getElementById('price' + idstr).innerHTML;
        cart[idstr] = [qty, name, parseInt(itemPrice)];
    }
    updateCart(cart);
});