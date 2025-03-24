// front/map.js
// 전역 변수 선언
let sikdangs; // 식당 데이터 저장
let map; // 지도 객체
let babzipMarkers = []; // 밥집 마커 배열
let cafeMarkers = []; // 카페 마커 배열
let sulzipMarkers = []; // 술집 마커 배열

// 식당 가져오고 지도 표시하기
async function getConfig() {
    try {
        const response = await fetch('/api/config');
        const data = await response.json();
        sikdangs = data.restaurants;
        initMap();
    } catch (error) {
        console.error('설정 로드 실패:', error);
    }
}

// 이미지 경로 반환
function imageSrc(type) {
    if (type == "술집") { return "../image/sulzip.png"; }
    else if (type == "카페") { return "../image/cafe.png"; }
    else { return "../image/babzip.png"; }
}

// 인포윈도우 반환
function InfoWindow(name, main_menu, address, reels_link) {
    const content = `<div class="info-window-content">
        <h2>${name}</h2>
        <p><strong>메인 메뉴:</strong> ${main_menu.join(", ")}</p>
        <p><strong>주소:</strong> ${address}</p>
        <div class="info-window-buttons">
            <a href="${reels_link}" target="_blank" rel="noopener noreferrer" class="info-window-button">인스타그램 릴스</a>
            <a href="https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(name)}" target="_blank" rel="noopener noreferrer" class="info-window-button">구글 지도</a>
            <a href="https://map.naver.com/v5/search/${encodeURIComponent(name)}" target="_blank" rel="noopener noreferrer" class="info-window-button">네이버 지도</a>
            <a href="https://map.kakao.com/?q=${encodeURIComponent(name)}" target="_blank" rel="noopener noreferrer" class="info-window-button">카카오맵</a>
        </div>
    </div>`;
    return content;
}

function setMarker(type, mapInstance) {
    if (type == "술집") {
        for (var i = 0; i < sulzipMarkers.length; i++) {
            sulzipMarkers[i].setMap(mapInstance);
        }
    } else if (type == "카페") {
        for (var i = 0; i < cafeMarkers.length; i++) {
            cafeMarkers[i].setMap(mapInstance);
        }
    } else {
        for (var i = 0; i < babzipMarkers.length; i++) {
            babzipMarkers[i].setMap(mapInstance);
        }
    }
}

function showMarker(type) {

    var babzipMenu = document.getElementById('babzipMenu');
    var cafeMenu = document.getElementById('cafeMenu');
    var sulzipMenu = document.getElementById('sulzipMenu');

    if (type === "술집") {
        if (sulzipMenu.className == 'menu_selected') {
            sulzipMenu.className = '';
            setMarker(type, null);
        } else {
            sulzipMenu.className = 'menu_selected';
            setMarker(type, map);
        }

    } else if (type === "카페") {
        if (cafeMenu.className == 'menu_selected') {
            cafeMenu.className = '';
            setMarker(type, null);
        } else {
            cafeMenu.className = 'menu_selected';
            setMarker(type, map);
        }
    } else {
        if (babzipMenu.className == 'menu_selected') {
            babzipMenu.className = '';
            setMarker(type, null);
        } else {
            babzipMenu.className = 'menu_selected';
            setMarker(type, map);
        }
    }
}

// 지도 시작하기
function initMap() {
    console.log("initMap");
    var mapContainer = document.getElementById('map'), // 지도를 표시할 div  
        mapOption = {
            center: new kakao.maps.LatLng(37.4562557, 126.7052062), // 지도의 중심좌표
            level: 8 // 지도의 확대 레벨
        };

    map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다

    var imageSize = new kakao.maps.Size(24, 35);
    var lat, lng;

    sikdangs.forEach(function(sikdang, i) {

        lat = sikdang["latitude"];
        lng = sikdang["longitude"];

        if (lat != 0 && lng != 0) {
            var markerImage = new kakao.maps.MarkerImage(imageSrc(sikdang["type"]), imageSize);
            var marker = new kakao.maps.Marker({
                map: map, // 마커를 표시할 지도
                position: new kakao.maps.LatLng(lat, lng), // 마커를 표시할 위치
                title: sikdang["name"], // 마커의 타이틀, 마커에 마우스를 올리면 타이틀이 표시됩니다
                image: markerImage
            });
            var infowindow = new kakao.maps.InfoWindow({
                content: InfoWindow(sikdang["name"], sikdang["main_menu"], sikdang["address"], sikdang["reels_link"]),
                removable: true
            });

            if (sikdang["type"] == "술집") { sulzipMarkers.push(marker); console.log("술집 추가"); }
            else if (sikdang["type"] == "카페") { cafeMarkers.push(marker); console.log("카페 추가"); }
            else { babzipMarkers.push(marker); console.log("밥집 추가"); }

            kakao.maps.event.addListener(marker, 'click', function() {
                // 마커 위에 인포윈도우를 표시합니다
                infowindow.open(map, marker);
            });
        };
    });
    document.getElementById('babzipMenu').classList.add('menu_selected');
    document.getElementById('cafeMenu').classList.add('menu_selected');
    document.getElementById('sulzipMenu').classList.add('menu_selected');
    setMarker("밥집", map);
    setMarker("카페", map);
    setMarker("술집", map);
}

getConfig();