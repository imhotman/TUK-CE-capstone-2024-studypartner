/* EXPANDER MENU */
const showMenu = (toggleId, navbarId, bodyId) => {
    const toggle = document.getElementById(toggleId),
    navbar = document.getElementById(navbarId),
    bodypadding = document.getElementById(bodyId)

    if( toggle && navbar ) {
        toggle.addEventListener('click', ()=>{
            navbar.classList.toggle('expander');

            bodypadding.classList.toggle('body-pd')
        })
    }
}

showMenu('nav-toggle', 'navbar', 'body-pd')

/* LINK ACTIVE */
const linkColor = document.querySelectorAll('.nav__link')
function colorLink() {
    linkColor.forEach(l=> l.classList.remove('active'))
    this.classList.add('active')
}
linkColor.forEach(l=> l.addEventListener('click', colorLink))

/* COLLAPSE MENU */
const linkCollapse = document.querySelectorAll('.collapse__link ion-icon[name="chevron-down-outline"]');

linkCollapse.forEach(icon => {
    icon.addEventListener('click', function() {
        const collapseMenu = this.parentElement.nextElementSibling;
        collapseMenu.classList.toggle('showCollapse');

        const rotate = this;
        rotate.classList.toggle('rotate');
    });
});

/* 내 강의 하위메뉴 추가하는 코드 */
document.getElementById('collapse-link').addEventListener('click', function() {
    const collapseMenu = document.getElementById('collapse-menu');
    
    // 사용자로부터 입력 받기
    const newItemName = prompt("새로운 강의명을 입력하세요:");
    if (!newItemName) return; // 입력이 없으면 동작하지 않음
    
    // 새로운 항목 추가
    const newMenuItem = document.createElement('li');
    const newLink = document.createElement('a');
    newLink.href = '#';
    newLink.classList.add('collapse__sublink');
    newLink.textContent = newItemName; // 사용자가 입력한 문자열을 그대로 항목에 추가
    newMenuItem.appendChild(newLink);
    collapseMenu.appendChild(newMenuItem);
});

/* 내 강의 이름 변경하는 코드 */
document.addEventListener('DOMContentLoaded', function() {
    // 내 강의 클릭 시 동작
    document.getElementById('my-courses').addEventListener('click', function() {
        const newName = prompt("변경할 강의의 이름을 입력하세요:", this.textContent);
        if (!newName) return;

        this.textContent = newName; // 내 강의 요소의 이름 변경
    });
});





