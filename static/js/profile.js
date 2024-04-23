var userDropdown = document.getElementById("user-dropdown");
var userDropdownMenu = document.getElementById("user-dropdown-menu");
userDropdown.addEventListener("click", function (event) {
    event.preventDefault();
    if (userDropdownMenu.style.display === "block") {
        userDropdownMenu.style.display = "none";
    } else {
        userDropdownMenu.style.display = "block";
    }
});