/* EXPANDER MENU */
const showMenu = (toggleId, navbarId, bodyId) => {
    const toggle = document.getElementById(toggleId),
        navbar = document.getElementById(navbarId),
        bodypadding = document.getElementById(bodyId)

    if (toggle && navbar) {
        toggle.addEventListener('click', () => {
            navbar.classList.toggle('expander');
            bodypadding.classList.toggle('body-pd');
        });
    }
}

showMenu('nav-toggle', 'navbar', 'body-pd');

/* LINK ACTIVE */
const linkColor = document.querySelectorAll('.nav__link');

function colorLink() {
    linkColor.forEach(l => l.classList.remove('active'))
    this.classList.add('active')
}

linkColor.forEach(l => l.addEventListener('click', colorLink));

/* COLLAPSE MENU */
const linkCollapse = document.querySelectorAll('.collapse__link ion-icon[name="chevron-down-outline"]');

linkCollapse.forEach(icon => {
    icon.addEventListener('click', function () {
        const collapseMenu = this.parentElement.nextElementSibling;
        collapseMenu.classList.toggle('showCollapse');

        const rotate = this;
        rotate.classList.toggle('rotate');
    });
});

/* 내 강의 하위메뉴 추가하는 코드 */
document.getElementById('collapse-link').addEventListener('click', function () {
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

// /* 내 강의 이름 변경하는 코드 */
// document.addEventListener('DOMContentLoaded', function () {
//     // 내 강의 클릭 시 동작
//     const myCoursesElement = document.getElementById('my-courses');
//     let isPromptShown = false; // 한 번만 prompt가 보이도록 하기 위한 변수

//     myCoursesElement.addEventListener('click', function () {
//         if (!isPromptShown) {
//             const newName = prompt("변경할 강의의 이름을 입력하세요:", this.textContent);
//             if (!newName) return;

//             this.textContent = newName; // 내 강의 요소의 이름 변경
//             isPromptShown = true; // prompt가 한 번 보였음을 표시
//         }
//     });
// });



/* 새로운 강의 추가하는 코드 */
document.getElementById('add_button').addEventListener('click', function () {
    const confirmation = confirm("새로운 강의를 추가하시겠습니까?");
    if (!confirmation) return; // 사용자가 취소를 선택하면 함수 종료

    // 내 강의 요소 생성
    const courseId = 'course-' + Date.now(); // 강의별 고유한 ID 생성

    const newCourseElement = document.createElement('div');
    newCourseElement.classList.add('nav__link', 'collapse');

    const folderIcon = document.createElement('ion-icon');
    folderIcon.setAttribute('name', 'folder-outline');
    folderIcon.classList.add('nav__icon');
    newCourseElement.appendChild(folderIcon);

    const spanElement = document.createElement('span');
    spanElement.classList.add('nav_name');
    spanElement.textContent = "새로운 강의"; // 새로운 강의 추가
    spanElement.id = courseId;
    newCourseElement.appendChild(spanElement);

    const collapseLink = document.createElement('div');
    collapseLink.classList.add('collapse__link');

    const addIcon = document.createElement('ion-icon');
    addIcon.setAttribute('name', 'add');
    collapseLink.appendChild(addIcon);

    const space = document.createTextNode(" "); // 공백 추가
    collapseLink.appendChild(space);

    const chevronIcon = document.createElement('ion-icon');
    chevronIcon.setAttribute('name', 'chevron-down-outline');
    chevronIcon.id = 'collapse-link2-' + courseId; // 강의별 고유한 ID 생성
    collapseLink.appendChild(chevronIcon);

    newCourseElement.appendChild(collapseLink);

    const ulElement = document.createElement('ul');
    ulElement.classList.add('collapse__menu', 'text_element');
    ulElement.id = 'collapse-menu2-' + courseId; // 강의별 고유한 ID 생성
    newCourseElement.appendChild(ulElement);

    // 새로 생성한 내 강의 요소를 문서에 추가
    const navList = document.querySelector('.nav__list');
    navList.insertBefore(newCourseElement, navList.children[2]); // 내 강의 바로 위에 삽입

    // "^" 아이콘 클릭 시 동작
    document.getElementById('collapse-link2-' + courseId).addEventListener('click', function () {
        const collapseMenu = document.getElementById('collapse-menu2-' + courseId); // 해당 강의의 하위 메뉴를 선택
        collapseMenu.classList.toggle('showCollapse');

        // 방향 전환을 위한 클래스 추가/제거
        this.classList.toggle('rotate');
    });

    // 내 강의 클릭 시 동작
    const newCourseSpan = document.getElementById(courseId);
    newCourseSpan.addEventListener('click', function () {
        const newName = prompt("변경할 강의의 이름을 입력하세요:", this.textContent);
        if (newName === null || newName === "" || newName === "새로운 강의") return; // 취소 또는 빈 문자열 처리

        this.textContent = newName; // 내 강의 요소의 이름 변경
    });

    // "+" 아이콘 클릭 시 동작
    addIcon.addEventListener('click', function () {
        const newItemName = prompt("추가할 항목의 이름을 입력하세요:");

        // 새로운 항목명이 비어있거나 취소를 누르면 종료
        if (!newItemName) return;

        // 새로운 항목 추가
        const newMenuItem = document.createElement('li');
        const newLink = document.createElement('a');
        newLink.href = '#'; // 여기를 원하는 링크로 수정하세요
        newLink.textContent = newItemName; // 사용자가 입력한 문자열을 그대로 항목에 추가
        newLink.classList.add('collapse__sublink'); // collapse__sublink 클래스 추가
        newMenuItem.appendChild(newLink); // a 요소를 li 요소에 추가
        const collapseMenu = document.getElementById('collapse-menu2-' + courseId);
        collapseMenu.appendChild(newMenuItem);


        // 새로 생성된 링크에 클릭 이벤트 핸들러 추가
         newLink.addEventListener('click', function(event) {
            event.preventDefault(); // 링크의 기본 동작 취소
            window.location.href = newLink.href; // 네이버로 이동
        });
    });
});


