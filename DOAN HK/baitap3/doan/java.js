/*
function openE() {
    let openE = document. getElementById ("openE") ;
    let closeE = document.getElementById ("closeE") ;
    password. type = "text";
    openE.style.display = "none";
    closeE.style.display = "block";
    }
    function closeE() {
    let openE = document. getElementById ("openE" );
    let closeE = document.getElementById ("closeE") ;
    password. type = "password" ;
    closeE. style.display = "none";
    openE. style.display = "block";
    }
    function submitForm() {
    let fullName = document.getElementById ("'fullName") ;
    let userName = document.getElementById ("userName" ) ;
    let emailId = document-getElementById ("emailId");
    let phoneNum = document-getElementById ("phoneNum" );
    let password = document-getElementById ("password");
    let confirmPass = document.getElementById ("confirmPass");
    if (
        fulIName.value ==
        userName.value == " " ||
        emailId.value == "" ||
        phoneNum.value == "" ||
        password.value == ""
    ) {
    alert("Enter your details!");
}   else {
document.getElementById ("container") .style.display = "none";
document.getElementById ("thank-you-container").style.display = "block";
}
    }
function submitForm(){
document.getElementById("container").style.disp
lay = "none";
document. getElementById ("thank-you-container").style.display = "block";
}
function goBack() {

document.getElementById ("container") .style.disp
lay = "block";
document.getElementById ("thank-you-container").style.display = "none";
}
*/


function openE() {
    let openE = document.getElementById("openE");
    let closeE = document.getElementById("closeE");
    let password = document.getElementById("password");

    password.type = "text"; // Hiện mật khẩu
    openE.style.display = "none"; // Ẩn biểu tượng mắt mở
    closeE.style.display = "block"; // Hiện biểu tượng mắt đóng
}

function closeE() {
    let openE = document.getElementById("openE");
    let closeE = document.getElementById("closeE");
    let password = document.getElementById("password");

    password.type = "password"; // Ẩn mật khẩu
    closeE.style.display = "none"; // Ẩn biểu tượng mắt đóng
    openE.style.display = "block"; // Hiện biểu tượng mắt mở
}

function submitForm() {
    // Lấy các giá trị từ ô nhập
    const fullName = document.getElementById("fullName").value.trim();
    const userName = document.getElementById("userName").value.trim();
    const emailId = document.getElementById("emailId").value.trim();
    const phoneNum = document.getElementById("phoneNum").value.trim();
    const password = document.getElementById("password").value;
    const confirmPass = document.getElementById("confirmPass").value;

    // Kiểm tra tất cả các trường đầu vào
    if (!fullName || !userName || !emailId || !phoneNum || !password || !confirmPass) {
        alert("Please fill out all fields.");
    } else if (password !== confirmPass) {
        alert("Passwords do not match!");
    } else {
        // Nếu tất cả hợp lệ, chuyển đến trang thank_you.html
        href = 'thank_you.html'; // Chuyển hướng đến trang cảm ơn
    }
}

function goBack() {
    // Hiện lại form đăng ký và ẩn thông báo cảm ơn
    document.getElementById("container").style.display = "block";
    document.getElementById("thank-you-container").style.display = "none";
}
