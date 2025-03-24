// front/app.js
const express = require('express')
const path = require('path')
const fs = require('fs').promises
const app = express()
const port = 3000

// views 디렉토리 설정 - front 폴더 안에 있으므로 상위 디렉토리로 이동
app.set('view engine', 'ejs'); 
app.set('views', path.join(__dirname, 'public/views')); 
// 정적 파일 제공
app.use(express.static(__dirname+'/public'))

// 메인 페이지 라우트
app.get('/', async (req, res) => {
    try {
        // front 폴더에서 상위 디렉토리의 data 폴더로 접근
        const data = await fs.readFile(path.join(__dirname, '../data/secret.json'), 'utf8')
        const config = JSON.parse(data)
        const mapApiKey = config.MAP_API_KEY
        
        res.render('index', { mapApiKey: mapApiKey })
    } catch (error) {
        console.error('구체적인 에러:', error)
        res.status(500).send('Error loading API key: ' + error.message)
    }
})

app.get('/api/config', async (req, res) => {
    try {
        const data = await fs.readFile(path.join(__dirname, '../data/restaurants_infos.json'), 'utf8');
        res.json(JSON.parse(data));
    } catch (error) {
        res.status(500).json({ error: '파일 읽기 실패' });
    }
});

app.listen(port, () => {
    console.log(`서버가 http://localhost:${port} 에서 실행 중입니다.`)
})