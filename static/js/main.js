function changeImg(smallImg) {
  var fullImg = document.getElementById("imageBox");
  fullImg.src = smallImg.src;
}
$(document).ready(function () {
  // Shop go to top button
  $(window).scroll(function () {
    var _scroll = window.scrollY;
    if (_scroll >= 500) {
      $(".top-icon").fadeIn();
    } else {
      $(".top-icon").fadeOut();
    }
  });

  // Rating (Star)
  rate = [];
  rating = $(".rating").text();
  for (let i = 0; i < rating; i++) {
    rate.push('<i class="fas fa-star"></i>');
  }
  if (rate.length < 5) {
    addBlankStar = 5 - rate.length;
    for (let i = 0; i < addBlankStar; i++) {
      rate.push('<i class="fal fa-star"></i>');
    }
    $(".rating").html(rate);
  }

  // Cart Price
  $.ajax({
    url: "/check_cart_price",
    dataType: "json",
    success: function (response) {
      $(".cartPrice").text(response["sum"]);
    },
  });

  // Wishlist
  $(".whishlist-btn").on("click", function () {
    var _pid = $(this).attr("data-product");
    $.ajax({
      url: "/add_wishlist",
      data: {
        product: _pid,
      },
      dataType: "json",
    });
  });

  // Cart
  $(".btn-cart").on("click", function () {
    var _pid = $(this).attr("data-product");
    var _cartItem = $(".itemLen").val();
    if (_cartItem == 0) {
      alert("Please Select 1 or More Item for Add to Cart");
    } else {
      $.ajax({
        url: "/add_cart",
        data: {
          product: _pid,
          cartItem: _cartItem,
        },
        dataType: "json",
        success: function (response) {
          $(".itemLen").val(0);
        },
      });
    }
  });

  // Add to Cart From Wishlist
  $(".add_cart_from_wishlist").on("click", function () {
    var _pid = $(this).attr("data-product");
    var _cartItem = 1;
    $.ajax({
      url: "/add_cart",
      data: {
        product: _pid,
        cartItem: _cartItem,
      },
      dataType: "json",
      success: function (response) {
        window.location = "/removeFromWishlist/" + _pid;
      },
    });
  });

  window.localStorage.clear();

  $(".compare-btn").click(function (e) {
    var _pid = $(this).attr("data-product");
    if (window.localStorage.getItem("first_product") == null) {
      window.localStorage.setItem("first_product", _pid);
      alert("Please Select Second Product");
    } else if (window.localStorage.length == 1) {
      window.localStorage.setItem("second_product", _pid);
      var _prod1 = window.localStorage.getItem("first_product");
      var _prod2 = window.localStorage.getItem("second_product");
      window.location = `/compare_product/${_prod1}/${_prod2}`;
    } else {
      alert("You already Select two Product");
    }
  });

  const sr = ScrollReveal({
      origin : "top",
      distance : "60px",
      duration : 2500,
      delay : 400,
  })


  // About
  sr.reveal(".about .h4" ,  { delay: 100  , origin : "left"});
  sr.reveal(".about .t-14" ,  { delay: 300  , origin : "left"});
  sr.reveal(".about .about-img" ,  { delay: 300  , origin : "right"});
  sr.reveal(".about .about-img-grid" ,  { delay: 2000  , origin : "bottom"});
//   sr.reveal(".cart-nav" ,  { delay: 100  , origin : "bottom"});
//   sr.reveal(".search-nav" ,  { delay: 100  , origin : "bottom"});
//   sr.reveal(".contact-nav" ,  { delay: 100  , origin : "bottom"});
//   sr.reveal(".main-nav .nav-item" ,  { delay: 100  , origin : "bottom"});


  // Home Page
  sr.reveal(".card-delivery" ,  { delay: 500  , origin : "bottom"});
  sr.reveal(".img-card-home" ,  { delay: 500  , origin : "bottom"});
  sr.reveal(".carousel-new-items" ,  { delay: 500  , origin : "left"});
  sr.reveal(".carousel-new-items2" ,  { delay: 500  , origin : "right"});
  sr.reveal("#b-card-1" ,  { delay: 500  , origin : "left"});
  sr.reveal("#b-card-2" ,  { delay: 500  , origin : "right"});
  sr.reveal(".footer .col-md-3" ,  { delay: 500  , origin : "top"});
  sr.reveal(".copy-text" ,  { delay: 2000  , origin : "left"});
  sr.reveal(".credit-card" ,  { delay: 2000  , origin : "right"});

  // Shop Page
  sr.reveal(".shop-page .col-md-3" ,  { delay: 100  , origin : "bottom"});
});
