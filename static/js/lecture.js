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







document.getElementById('collapse-link').addEventListener('click', function() {
    const collapseMenu = document.getElementById('collapse-menu');
    
    // 사용자로부터 입력 받기
    const newItemName = prompt("새로운 항목의 이름을 입력하세요:");
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






