// carousel slideshow
// citation/sources used: https://www.w3schools.com/w3css/w3css_slideshow.asp
// auto scrolling
var currIndex = 0;
carousel();
function carousel() {
    var x = document.getElementsByClassName("slides");
    var dots = document.getElementsByClassName("dot");
    for (var i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    currIndex++;
    if (currIndex > x.length) {currIndex = 1}
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    x[currIndex-1].style.display = "block";
    dots[currIndex-1].className += " active";
    setTimeout(carousel, 6000);
}
// carousel button functionality 
// allows for unlimited button pushing of either direction
var slide = 1;
showDivs(slide);
function plusDivs(n) {
    showDivs(slide += n);
}
function currentSlide(n) {
    showDivs(slide = n);
}
function showDivs(n) {
    var x = document.getElementsByClassName("slides");
    var dots = document.getElementsByClassName("dot");
    if (n > x.length) {slide = x.length-2};
    if (n < 1) {slide = x.length};
    for (var i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    x[slide-1].style.display = "block";
    dots[slide-1].className += " active";
}
